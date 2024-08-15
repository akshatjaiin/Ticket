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

order = []  # The in-progress order.
placed_order = []  # The confirmed, completed order.

def user_details(name: str, age: int, student: bool) -> dict:
    """Store user details in a dictionary."""
    return {"name": name, "age": age, "student": student}

def add_to_order(name: str, modifiers: Iterable[str] = ()) -> None:
  """Adds the specified name to the customer's order, including any modifiers."""
  order.append((name, modifiers))


def get_order() -> Iterable[tuple[str, Iterable[str]]]:
  """Returns the customer's order."""
  return order


def remove_item(n: int) -> str:
  """Remove the nth (one-based) item from the order.

  Returns:
    The item that was removed.
  """
  item, modifiers = order.pop(int(n) - 1)
  return item


def clear_order() -> None:
  """Removes all items from the customer's order."""
  order.clear()


def confirm_order(name) -> str:
  """Asks the customer if the order is correct.

  Returns:
    The user's free-text response.
  """

  print(name)
  if not order:
    print('  (no items)')

  for name, modifiers in order:
    print(f'  {name}')
    if modifiers:
      print(f'   - {", ".join(modifiers)}')

  return input('Is this correct? ')


def place_order(name: str, student: bool, age: int) -> int:
    """Processes the payment and stores user details in a CSV file.

    Returns:
        Processing time for the order.
    """
    # Collect user details
    user_info = user_info(name, age, student)

    # Write user details to a CSV file
    with open('user_details.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "age", "student"])
        writer.writerow(user_info)

    # Move order to placed_order and clear the current order
    placed_order[:] = order.copy()
    clear_order()

    placed_order[:] = order.copy()
    clear_order()

  # TODO(you!): Implement ticket fulfilment.
    return randint(1, 10)

# Alternative encodings to try if UTF-8 doesn't work
MUSEUM_BOT_PROMPT = open("new_prompt.txt", "r", encoding="ISO-8859-1").read()

ordering_system = [add_to_order, user_details, get_order, remove_item, clear_order, confirm_order, place_order]

# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False

model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'

if use_sys_inst:
  model = genai.GenerativeModel(
      model_name, tools=ordering_system, system_instruction=MUSEUM_BOT_PROMPT)
  convo = model.start_chat(enable_automatic_function_calling=True)

else:
  model = genai.GenerativeModel(model_name, tools=ordering_system)
  convo = model.start_chat(
      history=[
          {'role': 'user', 'parts': [MUSEUM_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ],
      enable_automatic_function_calling=True)


@retry.Retry(initial=30)
def send_message(message):
  return convo.send_message(message)

placed_order = []
order = []


while not placed_order:
  response = send_message(input('> '))
  print(response.text)

# giving to much errors
