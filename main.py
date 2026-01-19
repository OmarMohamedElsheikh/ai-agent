import os 
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions , call_function


def main():

    load_dotenv()


    parser = argparse.ArgumentParser(
        prog="gimini-api agent",
        description="ai-agent chatbot",
        
    )

    parser.add_argument("user_prompt", type=str , help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    verbose = args.verbose

    messages = [genai.types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

    api_key = os.environ.get("GIMINI_API_KEY")
    if not api_key :
        raise RuntimeError("api key not found or not initialized!")

    client = genai.Client(api_key=api_key)
    for _ in range(20):
        content = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
        )
        
        
        if content.candidates:
            for cand in content.candidates :
                if cand.content:
                    messages.append(cand.content)

        function_calls = content.function_calls

        

        if not content.usage_metadata :
            raise RuntimeError("faild request!")

        if args.verbose:
            print("User prompt: " , args.user_prompt )
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
            return 

            
        if functions_results:
            messages.append(
                types.Content(
                    role="user",
                    parts=functions_results
            )
        )
    print("Stopped: reached maximum iterations (20).")
    return 1

if __name__ == "__main__":
    main()
