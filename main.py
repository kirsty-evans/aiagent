
# to load environment variables from the .env file
import os
import sys
from dotenv import load_dotenv 
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

# system prompt instructs the AI how to behave and respond despite what the user prompt is
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# user enters their prompt as a command line argument - uv run main.py {prompt}
user_prompt = sys.argv[1]

#list of types.Content with user prompt, to store list of messages later
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# list of all available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# loads environment variables from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# creates new instance of a Gemini client
client = genai.Client(api_key=api_key)

# generate content method to get a response from AI
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
	config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

# prints the AI response
# first checks if the AI response contains function calls
if response.function_calls:
	for function_call_part in response.function_calls:
		print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
	# generate_content returns an object, so convert to text to see the AI answer
	print(response.text)

# prints number of tokens consumed by the interaction
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

# use --verbose to see more info
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
	print(f"User prompt: {user_prompt}")
	print(f"Prompt tokens: {prompt_tokens}")
	print(f"Response tokens: {response_tokens}")



