import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    verbose_flag = False
    cli_args = len(sys.argv)
    max_calls = 20
    model_name = 'gemini-2.0-flash-001'

    system_prompt = """
    You are a helpful AI coding agent.

    You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write to files
    - Run python files

    Try your best to complete the user request.

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """ 

    if cli_args > 1:
        user_prompt = sys.argv[1]
    else:
        print("No prompt was entered.")
        sys.exit(1)

    for i in range(1, cli_args):
        if sys.argv[i] == "--verbose":
            verbose_flag = True

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(1, max_calls):
        response = client.models.generate_content(
            model=model_name,
            contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt,
            ),
        )

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose_flag)
                messages.append(function_call_result.parts[0])
                if function_call_result.parts[0].function_response.response:
                    if verbose_flag == True:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("Response was empty")
        else:
            print(response.text)
            break

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if verbose_flag:
        print("Prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
