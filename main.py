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
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    # --- TO PASS THE TEST (GPT GENERATED) ---
    # messages = [
    # types.Content(
    #     role="user",
    #     parts=[types.Part(
    #         text=f"{system_prompt}\n\nUser input:\n{args.user_prompt}"
    #     )]
    #     )
    # ]


    


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        #config = types.GenerateContentConfig(system_instruction = system_prompt)
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    )

    #To check if tokens are generated
    if response.usage_metadata is None:
        raise RuntimeError(
            "Failed API request, No tokens generated!"
        )
    else:
        if args.verbose:
            #to keep a track of number of tokens used
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print("User prompt:",args.user_prompt)
            print("Prompt tokens:",prompt_tokens)
            print("Response tokens:",response_tokens)
            # Handle function calls if present
            function_results = []

            if response.function_calls:
                for function_call in response.function_calls:

                    # Execute the function via dispatcher
                    function_call_result = call_function(
                        function_call,
                        verbose=args.verbose,
                    )

                    # Defensive checks
                    if not function_call_result.parts:
                        raise RuntimeError("Function call returned no parts")

                    function_response = function_call_result.parts[0].function_response
                    if function_response is None:
                        raise RuntimeError("Missing function_response")

                    response_payload = function_response.response
                    if response_payload is None:
                        raise RuntimeError("Function response payload is None")

                    # Store result
                    function_results.append(function_call_result.parts[0])

                    # Optional verbose logging
                    if args.verbose:
                        print(f"-> {response_payload}")

            else:
                # No function call → normal text response
                print(response.text)



if __name__ == "__main__":
    main()
