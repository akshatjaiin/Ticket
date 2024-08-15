from typing import List, Dict
from random import randint

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

def calculate_price(visitor: Visitor) -> float:
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


def test_gemini_museum_ticket_bot() -> None:
    """
    Test the functionalities of the Gemini Museum Ticket Bot.

    This function simulates adding bookings, viewing them, confirming,
    and finalizing the bookings to ensure all components of the bot
    are working as expected.
    """
    # Step 1: Add bookings
    print("Adding bookings...")
    add_booking("Alice", 30, "Female", "Indian")
    add_booking("Bob", 10, "Male", "Indian")
    add_booking("Charlie", 25, "Male", "American")

    # Step 2: View current bookings
    print("\nCurrent bookings:")
    bookings = get_booking()
    for booking in bookings:
        print(booking)

    # Step 3: Confirm bookings
    confirmation_response = confirm_booking()
    print(f"\nUser confirmation response: {confirmation_response}")

    # Step 4: Finalize bookings if confirmed
    if confirmation_response == 'yes':
        processing_time = finalize_booking()
        print(f"\nBookings confirmed! Estimated processing time: {processing_time} seconds")
    else:
        print("\nBookings not confirmed. No further action taken.")

    # Step 5: View confirmed bookings
    print("\nConfirmed bookings:")
    for booking in confirmed_booking:
        print(booking)

    # Step 6: Clear all bookings for a fresh start
    clear_booking()
    print("\nAll bookings cleared.")
    print(f"Current in-progress bookings: {get_booking()}")
    print(f"Current confirmed bookings: {confirmed_booking}")

# Run the test function
test_gemini_museum_ticket_bot()