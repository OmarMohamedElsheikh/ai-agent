import os 
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()


praser = argparse.ArgumentParser(
    prog="gimini-api agent",
    description="ai-agent chatbot",
    
)

praser.add_argument("user_prompt", type=str , help="user prompt")
args = praser.prase_args()


api_key = os.environ.get("GIMINI_API_KEY")
if not api_key :
    raise RuntimeError("api key not found or not initialized!")

client = genai.Client(api_key=api_key)

content = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = args.user_prompt
    
)
if not content.usage_metadata :
    raise RuntimeError("faild request!")


print("Prompt tokens:", content.usage_metadata.prompt_token_count)
print("Response tokens:", content.usage_metadata.candidates_token_count)

print(content.text)
