"""
tanker_core.py - Core logic for Swapi Water Tanker
Handles water dispensing state, capacity management, and validation.
"""

from typing import Tuple, List, Generator
import time

VALID_DENOMINATIONS: List[int] = [1, 2, 5, 10, 15, 20]
DEFAULT_TANK_CAPACITY: int = 1000  # Total capacity in litres


class WaterTanker:
    """Manages the state and dispensing operations of the water tanker."""

    def __init__(self, capacity: int = DEFAULT_TANK_CAPACITY):
        self.capacity: int = capacity
        self.current_water: int = capacity
        self.total_dispensed: int = 0
        self.transaction_history: List[dict] = []

    def validate_amount(self, amount_input: str, allow_custom: bool = False) -> Tuple[bool, int, str]:
        """
        Validates the user input amount.
        Returns: (is_valid: bool, parsed_amount: int, error_message: str)
        """
        # Strip whitespace
        cleaned = amount_input.strip() if isinstance(amount_input, str) else str(amount_input).strip()
        if not cleaned:
            return False, 0, "Input cannot be empty. Please enter an amount."

        # Parse integer
        try:
            amount = int(cleaned)
        except ValueError:
            return False, 0, "Invalid input! Please enter a whole integer number."

        if amount <= 0:
            return False, 0, "Amount must be greater than 0."

        if not allow_custom and amount not in VALID_DENOMINATIONS:
            valid_str = ", ".join(map(str, VALID_DENOMINATIONS))
            return False, 0, f"Invalid denomination! Standard amounts are: [{valid_str}]."

        if amount > self.current_water:
            return False, 0, (
                f"Insufficient water in tanker! Requested: {amount}L, "
                f"Available: {self.current_water}L. Please refill."
            )

        return True, amount, ""

    def refill(self, litres: int = None) -> int:
        """Refills the tanker to maximum or adds specified litres."""
        if litres is None or litres >= (self.capacity - self.current_water):
            added = self.capacity - self.current_water
            self.current_water = self.capacity
        else:
            added = max(0, litres)
            self.current_water = min(self.capacity, self.current_water + added)
        return added

    def dispense_stream(self, amount: int, step_delay: float = 0.3) -> Generator[Tuple[int, int, float], None, None]:
        """
        Generator that dispenses water litre-by-litre.
        Yields: (current_litre, total_litres, percent_complete)
        """
        if amount > self.current_water:
            raise ValueError("Cannot dispense more than available water.")

        for litre in range(1, amount + 1):
            if step_delay > 0:
                time.sleep(step_delay)
            self.current_water -= 1
            self.total_dispensed += 1
            percent = (litre / amount) * 100
            yield (litre, amount, percent)

        # Record transaction
        self.transaction_history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "litres": amount,
            "remaining_tank": self.current_water
        })
