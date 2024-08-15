import os
from random import randint
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, List
from google.api_core import retry

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Define the Visitor type
Visitor = Dict[str, str | int]

# Initialize lists for managing bookings
in_progress_booking: List[Visitor] = []
confirmed_booking: List[Visitor] = []

# Function to add a visitor's booking
def add_booking(name: str, age: int, gender: str, nationality: str) -> None:
    visitor = {"name": name, "age": age, "gender": gender, "nationality": nationality}
    in_progress_booking.append(visitor)

# Function to view the current bookings
def get_booking() -> List[Visitor]:
    return in_progress_booking

# Function to remove a booking
def remove_booking(n: int) -> Visitor:
    if 0 < n <= len(in_progress_booking):
        return in_progress_booking.pop(n - 1)
    else:
        raise IndexError("Booking index out of range.")

# Function to clear all bookings
def clear_booking() -> None:
    in_progress_booking.clear()

# Function to calculate the ticket price
def calculate_price(visitor: Visitor) -> float:
    try:
        age = visitor["age"]
        nationality = visitor["nationality"].lower()
    except KeyError as e:
        raise ValueError(f"Missing required visitor information: {e}")

    base_price = 50.0
    child_price = 25.0
    foreign_price = 200.0

    if age < 12:
        return child_price
    elif nationality != "indian":
        return foreign_price
    return base_price

# Function to confirm the booking
def confirm_booking() -> str:
    print('Your current bookings:')
    if not in_progress_booking:
        print('  (no bookings)')
    for visitor in in_progress_booking:
        name = visitor["name"]
        age = visitor["age"]
        gender = visitor["gender"]
        nationality = visitor["nationality"]
        price = calculate_price(visitor)
        print(f'  {name}, Age: {age}, Gender: {gender}, Nationality: {nationality} - Ticket Price: ₹{price:.2f}')
    return input('Is this correct? (yes/no) ').strip().lower()

# Function to finalize the booking
def finalize_booking() -> int:
    confirmed_booking[:] = in_progress_booking.copy()
    clear_booking()
    return randint(5, 15)

MUSEUM_BOT_PROMPT = """..."""  # Same prompt as before

# Define booking system functions for integration
booking_system = [add_booking, get_booking, remove_booking, clear_booking, calculate_price, confirm_booking, finalize_booking]

# Toggle between models
use_sys_inst = False
model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'

model = genai.GenerativeModel(
    model_name=model_name,
    tools=booking_system,
    system_instruction=MUSEUM_BOT_PROMPT if use_sys_inst else None
)
convo = model.start_chat(enable_automatic_function_calling=True)

@retry.Retry(initial=30)
def send_message(message):
    return convo.send_message(message)

print('Welcome to MUSEUM bot!\n\n')

while not confirmed_booking:
    user_input = input('> ')
    response = send_message(user_input)
    print(response.text)
