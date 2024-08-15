# Basic imports
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# modal api 
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)
query = input("ask me something: ")

# Print chunks of the response as they arrive
response = chat_session.send_message(query, stream=True)
for chunk in response:
  print(chunk.text, end="")