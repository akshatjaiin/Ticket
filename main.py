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

order = {}  # The in-progress order.
placed_order = []  # The confirmed, completed order.

def name(name: str) -> None:
  """add name to our order"""
  order["name"] = name

def age(age: int) -> None:
  "add age to our order"
  order["age"] = age

def nationality(indian: bool):
  "check if the user is indian or not"
  order["indian"] = indian

def date(date: str):
  "scedulate users booking"
  order["date"] = date
  
def student(student: bool):
  "check if the user is student or not"
  order["student"] = student

def ticket_type(ticket_type: str):
  "ask the user what kind of ticket he wants"
  order["ticket_type"] = ticket_type

def get_order() -> Iterable[tuple[str, Iterable[str]]]:
  """Returns the customer's order."""
  return order

def remove_item(key: str) -> None:
    """Remove an item from the order by its key."""
    global order
    print(f"order content before removal: {order}")
    
    if key in order:
        removed_value = order.pop(key)
        print(f"Removed {key}: {removed_value} from the order.")
    else:
        print(f"Key '{key}' not found in the order.")
    
    print(f"order content after removal: {order}")

def clear_order() -> None:
  """Removes all items from the customer's order."""
  order.clear()

def confirm_order() -> str:
  """Asks the customer if the order is correct.
  Returns:
    The user's free-text response.
  """
  print(order)
  if not order:
    print('  (no items)')

  return input('Is this correct? ')


def place_order() -> int:
  """first enter the users detail in csv
    Returns:
    
    processing the payment.
  """
        
    # Write user details to a CSV file
  with open('user_details.csv', mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["name", "age", "student", "nationality", "indian", "date"])
    writer.writerow(order)
  placed_order[:] = order.copy()
  clear_order()

  # TODO(you!): Implement ticket fulfilment.
  return randint(1, 10)

# Alternative encodings to try if UTF-8 doesn't work
MUSEUM_BOT_PROMPT = open("new_prompt.txt", "r", encoding="ISO-8859-1").read()

# Define the ordering system tools/functions
ordering_system = [name, age, nationality, date, student, ticket_type, get_order, remove_item, clear_order, confirm_order, place_order]

# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False

# Select the model name based on the toggle
model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'
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
        model_name, tools=ordering_system, system_instruction=MUSEUM_BOT_PROMPT, safety_settings=safe)
    convo = model.start_chat(enable_automatic_function_calling=True)
else:
    model = genai.GenerativeModel(model_name, tools=ordering_system, safety_settings=safe)
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
    try:
        user_input = input('> ')
        response = send_message(user_input)
        print(response.text)

        # Here you might want to check if the order is placed and update placed_order accordingly
        # Example: if response indicates order confirmation, you could set placed_order to True

    except Exception as e:
        print(f"An error occurred: {e}")