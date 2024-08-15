#  using gemini cookbook brista bots perspective

import os
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

def add_to_order(drink: str, modifiers: Iterable[str] = ()) -> None:
  """Adds the specified ticket to the customer's order, including any modifiers."""
  order.append((drink, modifiers))


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


def confirm_order() -> str:
  """Asks the customer if the order is correct.

  Returns:
    The user's free-text response.
  """

  print('Your order:')
  if not order:
    print('  (no items)')

  for drink, modifiers in order:
    print(f'  {drink}')
    if modifiers:
      print(f'   - {", ".join(modifiers)}')

  return input('Is this correct? ')


def place_order() -> int:
  """Submit the order for further processing.

  Returns:
    processing the payment.
  """
  placed_order[:] = order.copy()
  clear_order()

  # TODO(you!): Implement coffee fulfilment.
  return randint(1, 10)


MUSEUM_BOT_PROMPT = open("bot_prompt.txt", "r").read()
