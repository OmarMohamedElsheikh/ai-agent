import os 
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


load_dotenv()


parser = argparse.ArgumentParser(
    prog="gimini-api agent",
    description="ai-agent chatbot",
    
)

parser.add_argument("user_prompt", type=str , help="user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()


messages = [genai.types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

api_key = os.environ.get("GIMINI_API_KEY")
if not api_key :
    raise RuntimeError("api key not found or not initialized!")

client = genai.Client(api_key=api_key)

content = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = messages,
)


if not content.usage_metadata :
    raise RuntimeError("faild request!")

if args.verbose:
    print("User prompt: " , args.user_prompt )
    print("Prompt tokens:", content.usage_metadata.prompt_token_count)
    print("Response tokens:", content.usage_metadata.candidates_token_count)

print(content.text)
