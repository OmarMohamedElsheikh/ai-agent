import os 
from dotenv import load_dotenv
from google import genai
load_dotenv()


api_key = os.environ.get("GIMINI_API_KEY")
if not api_key :
    raise RuntimeError("api key not found or not initialized!")

client = genai.Client(api_key=api_key)

content = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    
)
if not content.usage_metadata :
    raise RuntimeError("faild request!")


print("Prompt tokens:", content.usage_metadata.prompt_token_count)
print("Response tokens:", content.usage_metadata.candidates_token_count)

print(content.text)
