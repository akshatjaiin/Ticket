from typing import List, Tuple
from random import randint

# Initialize lists for managing bookings
in_progress_booking: List[Tuple[str, int]] = []  # (visitor_name, number_of_tickets)
confirmed_booking: List[Tuple[str, int]] = []

# Function to add a booking
def add_booking(visitor_name: str, tickets: int) -> None:
    """Add a booking for the specified visitor."""
    in_progress_booking.append((visitor_name, tickets))

# Function to view the current bookings
def get_booking() -> List[Tuple[str, int]]:
    """Returns the current booking."""
    return in_progress_booking

# Function to remove a booking
def remove_booking(n: int) -> Tuple[str, int]:
    """Remove the nth (one-based) booking."""
    booking = in_progress_booking.pop(int(n) - 1)
    return booking

# Function to clear all bookings
def clear_booking() -> None:
    """Removes all bookings."""
    in_progress_booking.clear()

# Function to confirm the booking
def confirm_booking() -> str:
    """Asks the customer if the booking is correct."""
    print('Your current bookings:')
    if not in_progress_booking:
        print('  (no bookings)')

    for visitor_name, tickets in in_progress_booking:
        print(f'  {visitor_name}: {tickets} ticket(s)')

    return input('Is this correct? ')

# Function to finalize the booking
def finalize_booking() -> int:
    """Submit the booking and return an estimated processing time."""
    confirmed_booking[:] = in_progress_booking.copy()
    clear_booking()

    # TODO: Implement further steps for booking processing.
    return randint(1, 10)
