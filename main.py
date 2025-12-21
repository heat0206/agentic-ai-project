import os
from dotenv import load_dotenv
from google import genai


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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    print(response.text)


if __name__ == "__main__":
    main()
