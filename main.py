
# to load environment variables from the .env file
import os
import sys
from dotenv import load_dotenv 
from google import genai
from google.genai import types


user_prompt = sys.argv[1]

#list of types.Content with user prompt, to store list of messages later
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# loads environment variables from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# creates new instance of a Gemini client
client = genai.Client(api_key=api_key)

# generate content method to get a response from AI
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

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
