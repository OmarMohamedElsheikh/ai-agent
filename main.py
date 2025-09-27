
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    if len(sys.argv) < 2 :
        print("usage: python3 main.py [prompet]")
        exit(1)
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    user_prompet = " ".join(sys.argv[1:])
    Messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompet)])
    ]
    load_dotenv()
    api_key= os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    def req(client,messages,verbose):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages
)
    
#        nonlocal vrep
        if verbose:
        
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print(f"User prompt: {user_prompt}\n")
        print(response.text)    
    req(client,Messages,verbose)
if __name__ == "__main__":
    main()
