
# to load environment variables from the .env file
import os
import sys
from dotenv import load_dotenv 
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file_content import schema_write_file
from functions.call_function import call_function, available_functions

# system prompt instructs the AI how to behave and respond despite what the user prompt is
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# user enters their prompt as a command line argument - uv run main.py {prompt}
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

#list of types.Content with user prompt, to store list of messages later
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# list of all available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
		schema_get_file_content, 
		schema_run_python_file, 
		schema_write_file
    ]
)

# loads environment variables from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# creates new instance of a Gemini client
client = genai.Client(api_key=api_key)

for i in range(20):
# generate content method to get a response from AI
	try:
		response = client.models.generate_content(
			model='gemini-2.0-flash-001', contents=messages,
			config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
		)

		for candidate in response.candidates:
			messages.append(candidate.content)

		# prints the AI response
		# first checks if the AI response contains function calls
		if response.function_calls:
			for function_call_part in response.function_calls:
				function_call_result = call_function(function_call_part)
				if (
					not function_call_result.parts
					or not getattr(function_call_result.parts[0], "function_response", None)
					or not getattr(function_call_result.parts[0].function_response, "response", None)
				):
					raise Exception("empty function call result")
				else:
					if verbose:
						print(f"-> {function_call_result.parts[0].function_response.response}")
				resp = function_call_result.parts[0].function_response.response
				resp_text = resp if isinstance(resp, str) else str(resp)
				messages.append(types.Content(role="user", parts=[types.Part(text=resp_text)]))
				

		else:
			# generate_content returns an object, so convert to text to see the AI answer
			print(response.text)
			break
	except Exception as e:
		print(f"Error: {e}")

# prints number of tokens consumed by the interaction
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

# use --verbose to see more info
if len(sys.argv) == 3 and verbose:
	print(f"User prompt: {user_prompt}")
	print(f"Prompt tokens: {prompt_tokens}")
	print(f"Response tokens: {response_tokens}")



