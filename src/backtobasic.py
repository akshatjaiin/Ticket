#  using gemini cookbook brista bots perspective
import csv
from random import randint
from typing import Iterable

class museum_bot:
    def __init__(self):
        self.order = {};
        self.placed_order = [];
    def name(self,name: str) -> None:
        """add name to our order"""
        self.order["name"] = name;

    def age(self,age: int) -> None:
        "add age to our order"
        self.order["age"] = age;

    def nationality(self,indian: bool):
        "check if the user is indian or not"
        self.order["indian"] = indian;

    def date(self,date: str):
        "scedulate users booking"
        self.order["date"] = date;

    def student(self,student: bool):
        "check if the user is student or not"
        self.order["student"] = student;

    def get_order(self) -> Iterable[tuple[str, Iterable[str]]]:
        """Returns the customer's order."""
        return self.order

    def remove_item(self,key: str) -> None:
        """Remove an item from the order by its key."""
        print(f"order content before removal: {self.order}")
    
        if key in self.order:
            removed_value = self.order.pop(key)
            print(f"Removed {key}: {removed_value} from the order.")
        else:
            print(f"Key '{key}' not found in the order.")
            print(f"order content after removal: {self.order}")

    def clear_order(self) -> None:
        """Removes all items from the customer's order."""
        self.order.clear()

    def confirm_order(self) -> str:
        """Asks the customer if the order is correct.
        Returns:
            The user's free-text response.
        """
        print(self.order)
        if not self.order:
            print('  (no items)')

        return input('Is this correct? ')

    def get_placed_order(self):
        return self.placed_order  ;
    def place_order(self) -> int:
        """first enter the users detail in csv
            Returns:
    
        processing the payment.
        """
        
        # Write user details to a CSV file
        with open('user_details.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "age", "student", "nationality", "indian", "date"])
        writer.writerow(order)
        self.placed_order = self.order.copy()
        clear_order()

        # TODO(you!): Implement ticket fulfilment.
        return randint(1, 10)
