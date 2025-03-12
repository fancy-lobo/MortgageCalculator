# tests/test_prepayment.py

import unittest
from unittest.mock import patch
from mortgage.prepayment import get_prepayment_schedule

class TestPrepayment(unittest.TestCase):
    @patch('builtins.input', side_effect=[
        "y",    # Equal prepayments? (y/yes)
        "1",    # Start month = 1
        "1",    # Frequency = 1 (monthly)
        "i",    # Number of intervals: type 'i' for indefinite
        "5000"  # Lump sum prepayment amount = $5,000
    ])
    def test_get_prepayment_schedule_indefinite(self, mock_inputs):
        # Assume total_payments is 360 (30 years x 12)
        schedule = get_prepayment_schedule(total_payments=360, filename="data/test_prepayment_details.json")
        # Expect intervals from month 1 to 360 with frequency 1 (i.e., 360 intervals).
        self.assertEqual(len(schedule), 360)
        # Check that a sample month has the correct prepayment amount.
        self.assertEqual(schedule[1], 5000)

if __name__ == '__main__':
    unittest.main()
