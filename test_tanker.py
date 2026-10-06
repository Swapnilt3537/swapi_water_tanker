"""
test_tanker.py - Unit tests for Swapi Water Tanker core functionality.
"""

import unittest
from tanker_core import WaterTanker, VALID_DENOMINATIONS


class TestWaterTanker(unittest.TestCase):
    def setUp(self):
        self.tanker = WaterTanker(capacity=100)

    def test_valid_standard_denominations(self):
        for denom in VALID_DENOMINATIONS:
            is_valid, parsed, err = self.tanker.validate_amount(str(denom))
            self.assertTrue(is_valid)
            self.assertEqual(parsed, denom)
            self.assertEqual(err, "")

    def test_invalid_denominations(self):
        # 3 is not in standard denominations
        is_valid, parsed, err = self.tanker.validate_amount("3", allow_custom=False)
        self.assertFalse(is_valid)
        self.assertIn("Invalid denomination", err)

    def test_custom_allowed(self):
        is_valid, parsed, err = self.tanker.validate_amount("42", allow_custom=True)
        self.assertTrue(is_valid)
        self.assertEqual(parsed, 42)

    def test_invalid_inputs(self):
        # Text input
        is_valid, _, err = self.tanker.validate_amount("abc")
        self.assertFalse(is_valid)
        self.assertIn("whole integer", err)

        # Empty input
        is_valid, _, err = self.tanker.validate_amount("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", err)

        # Negative and zero
        is_valid, _, err = self.tanker.validate_amount("-5")
        self.assertFalse(is_valid)
        is_valid, _, err = self.tanker.validate_amount("0")
        self.assertFalse(is_valid)

    def test_insufficient_water(self):
        self.tanker.current_water = 5
        is_valid, _, err = self.tanker.validate_amount("10")
        self.assertFalse(is_valid)
        self.assertIn("Insufficient water", err)

    def test_dispensing(self):
        initial_tank = self.tanker.current_water
        amount_to_dispense = 5
        dispensed_steps = list(self.tanker.dispense_stream(amount_to_dispense, step_delay=0.01))

        self.assertEqual(len(dispensed_steps), 5)
        self.assertEqual(dispensed_steps[-1], (5, 5, 100.0))
        self.assertEqual(self.tanker.current_water, initial_tank - 5)
        self.assertEqual(self.tanker.total_dispensed, 5)
        self.assertEqual(len(self.tanker.transaction_history), 1)

    def test_refill(self):
        self.tanker.current_water = 20
        added = self.tanker.refill()
        self.assertEqual(added, 80)
        self.assertEqual(self.tanker.current_water, 100)


if __name__ == "__main__":
    unittest.main()
