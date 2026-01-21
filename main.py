import os 
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions , call_function
from google.genai.errors import ClientError 

def main():

    load_dotenv()


    parser = argparse.ArgumentParser(
        prog="gimini-api agent",
        description="ai-agent chatbot",
        
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    verbose = args.verbose


    api_key = os.environ.get("GIMINI_API_KEY")
    if not api_key :
        raise RuntimeError("api key not found or not initialized!")

    client = genai.Client(api_key=api_key)

    messages = []
    
    while True:
        user_input = input("You: ")
        messages.append(genai.types.Content(role="user",parts=[types.Part(text=user_input)]))
        itra = 0

        for _ in range(20):
            itra += 1
            try : 
                content = client.models.generate_content(
                    model = "gemini-2.5-flash",
                    contents = messages,
                    config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt),
                )
            except ClientError as e:
                if e.code == 429 or "RESOURCE_EXHAUSTED" in str(e):
                    print("Quota exhusted. try later.")
                    return 1
                raise Exception(f"Error: {e}")
            
            if content.candidates:
                for cand in content.candidates :
                    if cand.content:
                        messages.append(cand.content)

            function_calls = content.function_calls

            

            if not content.usage_metadata :
                raise RuntimeError("faild request!")

            if args.verbose:
                print("Prompt tokens:", content.usage_metadata.prompt_token_count)
                print("Response tokens:", content.usage_metadata.candidates_token_count)

            functions_results = []

            if function_calls :
                
                for function_call in function_calls:

                    function_result = call_function(function_call,verbose)

                    if (
                        not function_result.parts
                        or not function_result.parts[0].function_response
                        ):

                        raise Exception("empty function call result")


                    if not function_result.parts[0].function_response.response:
                        raise Exception("function has not response")

                    functions_results.append(function_result.parts[0])

                    if verbose :
                        print(f"-> {function_result.parts[0].function_response.response}")
            else :
                print("Final response:\n")
                print(content.text)
                break

                
            if functions_results:
                messages.append(
                    types.Content(
                        role="user",
                        parts=functions_results
                )
            )
        if itra >= 20:
            print("Stopped: reached maximum iterations (20).")

            return 1

        continue_chat = input("Do you want to continue (y/n)? (anything except 'y' will exit)??").lower()
        if continue_chat != 'y':
            break
    print("exiting chat.")
    return 0

if __name__ == "__main__":
    main()
