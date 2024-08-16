import os
import csv
import json
from random import randint
from typing import Iterable
from dotenv import load_dotenv
from google.api_core import retry
import google.generativeai as genai

# cofiguring model api 
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
)

MUSEUM_BOT_PROMPT = '''i want you to extract user information from text and return it in a structured format.
your goal is to chat with user based on his user_info and give your response back to user inside a json within the user_info.
**json schema:**

user_info = {
 "name": str,
 "age": int,
 "indian": bool,
 "student": bool,
 "ticket_type": str,
 "date": str,
 "your_response": str,
 "response back to user": str,
}

Return Json, with respone
if any required fields are missing, please ask follow-up respone to gather the missing information before returning the JSON. Only return the JSON when all required fields are populated.

you can ask me respones until the json is fully populated.'''


# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False
# Select the model name based on the toggle
model_name = 'gemini-1.5-flash'
safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
# Initialize the model with safety settings
if use_sys_inst:
    model = genai.GenerativeModel(
        model_name, system_instruction=MUSEUM_BOT_PROMPT, safety_settings=safe, 
        generation_config= {'response_mime_type': "application/json"}
    )
    convo = model.start_chat(enable_automatic_function_calling=True)
else:
    model = genai.GenerativeModel(model_name, generation_config= {'response_mime_type': "application/json"}, safety_settings=safe)
    convo = model.start_chat(
        history=[
            {'role': 'user', 'parts': [MUSEUM_BOT_PROMPT]},
            {'role': 'model', 'parts': ['OK I will fill response back to user to continue chat with him.']}
        ],
        enable_automatic_function_calling=True
    )

@retry.Retry(initial=30)
def send_message(message):
    """Send a message to the conversation and return the response."""
    return convo.send_message(message)

# Initialize order tracking
placed_order = []
order = {}

# Main loop for user interaction
while True:
    user_input = input('> ')
    if user_input.lower() == "quit":
        break

    response = send_message(user_input)
    print(response.text)

    # Extract the JSON string from the response.
    json_string = response.text.strip() 

    # Convert the JSON string to a dictionary
    try:
        user_info = json.loads(json_string)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from Gemini.")
        continue

   
    print(user_info)