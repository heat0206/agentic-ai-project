import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from functions.call_function import available_functions
from functions.call_function import call_function





def main():
    #print("Hello from agentic-ai-project!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")


    #Code to check if enviorenment variable is not found
    if api_key is None:
        raise RuntimeError(
            "API_KEY environment variable not found. "
            "Please set it before running the application."
        )


    #Import the genai library and use the API key to create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    # creating a debug mode 
    parser.add_argument(
    "--verbose",
    action="store_true",
    help="Enable verbose output"    
    )
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    # we need a history of the previous conversations.
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        # --- Token logging (early) ---
        if response.usage_metadata and args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # --- Add model output to history ---
        for candidate in response.candidates:
            messages.append(candidate.content)

        function_responses=[]
        tool_called = False

        # --- Handle tool calls ---
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    tool_called = True
                    tool_response = call_function(
                        part.function_call,
                        verbose=args.verbose
                    )

                    function_responses.extend(tool_response.parts)
                    
        if tool_called:
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses
                )
            )


        # --- Stop if model is done ---
        if not tool_called:
            # Final answer reached
            for part in response.candidates[0].content.parts:
                if part.text:
                    print(part.text)
            return

    print("❌ Agent failed to reach a final response within 20 iterations.")
    sys.exit(1)



if __name__ == "__main__":
    main()
