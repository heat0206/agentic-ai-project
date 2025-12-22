import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


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

    


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
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
            print("Response:\n",response.text)        
            
        else:
            print(response.text)
    


if __name__ == "__main__":
    main()
