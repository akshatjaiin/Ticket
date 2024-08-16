#  using gemini cookbook brista bots perspective
import os
import csv
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

MUSEUM_BOT_PROMPT = '''I want you to extract user information from text and return it in a structured format. 
**JSON Schema:**
you are alowed to ask me questions untill the json is not null
USER_INFO = {
    "name": str, 
    "age": int,
    "indian": bool,
    "student": bool,
    "ticket_type": str,
    "date": str
    "your_question": str,
} '''



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
            {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
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
while not placed_order:
    user_input = input('> ')
    response = send_message(user_input)
    print(response.text)
