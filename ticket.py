# Basic imports
import os
from random import randint
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from typing import Dict, List
from google.api_core import retry
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


# Visitor structure
Visitor = Dict[str, str or int]

# Initialize lists for managing bookings
in_progress_booking: List[Visitor] = []
confirmed_booking: List[Visitor] = []

# Function to add a visitor's booking
def add_booking(name: str, age: int, gender: str, nationality: str) -> None:
    """
    Add a booking for the specified visitor.

    Parameters:
    - name (str): The name of the visitor.
    - age (int): The age of the visitor.
    - gender (str): The gender of the visitor.
    - nationality (str): The nationality of the visitor.
    
    This function creates a visitor dictionary and appends it to the 
    in_progress_booking list for further processing.
    """
    visitor = {
        "name": name,
        "age": age,
        "gender": gender,
        "nationality": nationality
    }
    in_progress_booking.append(visitor)

# Function to view the current bookings
def get_booking() -> List[Visitor]:
    """
    Returns the current bookings.

    Returns:
    - List[Visitor]: A list of visitors currently in progress of booking.
    
    This function provides the current state of bookings for 
    review before confirmation.
    """
    return in_progress_booking

# Function to remove a booking
def remove_booking(n: int) -> Visitor:
    """
    Remove the nth (one-based) booking.

    Parameters:
    - n (int): The one-based index of the booking to remove.

    Returns:
    - Visitor: The removed visitor's booking information.
    
    This function removes a specific booking from the 
    in_progress_booking list based on the provided index.
    """
    if 0 < n <= len(in_progress_booking):
        return in_progress_booking.pop(n - 1)
    else:
        raise IndexError("Booking index out of range.")

# Function to clear all bookings
def clear_booking() -> None:
    """
    Removes all bookings.

    This function clears the in_progress_booking list, 
    effectively resetting the booking process.
    """
    in_progress_booking.clear()

def calculate_price(visitor: dict) -> float:
    """
    Calculates the ticket price based on age, gender, and nationality.

    Parameters:
    - visitor (Visitor): A dictionary containing visitor details.

    Returns:
    - float: The calculated ticket price in INR.
    
    This function applies pricing rules based on the visitor's 
    age and nationality to determine the ticket price.
    """
    
    age = visitor["age"]
    nationality = visitor["nationality"].lower()  # Normalize to lowercase for comparison

    # Base prices (in INR)
    base_price = 50.0  # Adult
    child_price = 25.0  # Child (under 12)
    foreign_price = 200.0  # Foreign national
    try:
        age = visitor["age"]
        nationality = visitor["nationality"].lower()
        # Rest of the code
    except KeyError as e:
        raise ValueError(f"Missing required visitor information: {e}")

    # Determine ticket price based on age and nationality
    if age < 12:
        price = child_price
    elif nationality != "indian":  # Assuming 'indian' is the local nationality
        price = foreign_price
    else:
        price = base_price

    return price

# Function to confirm the booking
def confirm_booking() -> str:
    """
    Asks the customer if the booking is correct.

    Returns:
    - str: User's response indicating whether the booking is correct.
    
    This function displays all current bookings along with the 
    calculated ticket prices and prompts the user for confirmation.
    """
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
    """
    Submit the booking and return an estimated processing time.

    Returns:
    - int: Estimated processing time in seconds for the booking.
    
    This function copies the in-progress bookings to the confirmed 
    bookings list, clears the in-progress list, and simulates 
    processing time.
    """
    confirmed_booking[:] = in_progress_booking.copy()  # Copy current bookings to confirmed
    clear_booking()  # Clear in-progress bookings

    # Simulate processing time for booking confirmation
    return randint(5, 15)  # Return a random processing time between 5 to 15 seconds


MUSEUM_BOT_PROMPT = """
You are a helpful and informative chatbot for booking tickets to the Albert Hall Museum in Jaipur. 

**Your primary goal is to guide the user through the ticket booking process.**

**Here's what you need to know:**

* **Albert Hall Museum:**
    * **Location:**  Ram Niwas Garden, Jaipur, Rajasthan 302004
    * **Hours:** 10:00 AM - 5:00 PM (Closed on Fridays)
    * **Ticket Prices:**
        * Adults: ₹50
        * Children (under 12): ₹25
        * Foreign Nationals: ₹200

* **Booking Process:**
    * **Online Booking:** Not available at this time.
    * **On-Site Booking:** Tickets can be purchased at the museum entrance.
* **Important Notes:**
    * **Photography:** Photography is allowed inside the museum, but flash photography is prohibited.
    * **Food and Drink:** Food and drink are not allowed inside the museum.
    * **Pets:** Pets are not allowed inside the museum.

**Here are some helpful tips for responding to user requests:**

* **Be clear and concise in your responses.**
* **Avoid unnecessary chatter or irrelevant information.**
* **Always prioritize helping the user book their tickets.**
* **If the user asks for directions, provide a link to Google Maps.**
* **If the user asks for information beyond booking tickets, politely inform them that your focus is on booking tickets.**

**Example Conversation:**

**User:** I would like to book tickets to the Albert Hall Museum.
**You:**  Sure!  Tickets can be purchased at the museum entrance.  How many tickets would you like?

**User:**  I need tickets for two adults.
**You:**  Great! The cost for two adult tickets is ₹100.

**User:**  Can I pay with credit card?
**You:**  Unfortunately, we only accept cash at the museum entrance. 

**User:**  What are the museum hours?
**You:**  The Albert Hall Museum is open from 10:00 AM to 5:00 PM. Please note that the museum is closed on Fridays.

**User:**  Thanks!
**You:**  You're welcome!  Enjoy your visit to the Albert Hall Museum. 

**Remember, your primary goal is to help the user book their tickets smoothly and efficiently.** 
"""

booking_system = [add_booking, get_booking, remove_booking, clear_booking, calculate_price, confirm_booking, finalize_booking]
# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False

model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'

if use_sys_inst:
  model = genai.GenerativeModel(
      model_name, tools=booking_system, system_instruction=MUSEUM_BOT_PROMPT)
  convo = model.start_chat(enable_automatic_function_calling=True)

else:
  model = genai.GenerativeModel(model_name, tools=booking_system)
  convo = model.start_chat(
      history=[
          {'role': 'user', 'parts': [MUSEUM_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ],
      enable_automatic_function_calling=True)


@retry.Retry(initial=30)
def send_message(message):
  return convo.send_message(message)

print('Welcome to MUSEUM bot!\n\n')
confirmed_booking = []
Visitor = []
while not confirmed_booking:
  response = send_message(input('> '))
  print(response.text)