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

MUSEUM_BOT_PROMPT = open('bot_prompt.txt', 'r', encoding='utf-8').read()


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

# Main loop for user interaction
while True:
    user_input = input('> ').strip()
    if user_input.lower() == "quit":
        break

        

    if user_input != "":
        response = send_message(user_input)
        
        response_json = json.loads(response.text)
        print(response_json[0]["your_response_back_to_user"])

        if response_json[0]["confirm"] == True:
            print("\n\n\n\n")
            for i in response_json[0]["users"]:
                print(i['user_info'])
            print("\n\nprocessing to payment gateway ........")
            # with open('user_data.csv', 'a', newline='') as csvfile:
            #     writer = csv.DictWriter(csvfile, fieldnames=user_info.keys())
            #     if csvfile.tell() == 0: 
            #         writer.writeheader()
        
   
  
    


