# tests/test_mortgage_details.py

import os
import unittest
from os.path import abspath, join, dirname
from unittest.mock import patch
from utils.mortgage_details import get_mortgage_details

class TestMortgageDetails(unittest.TestCase):
    def setUp(self):
        # Compute the absolute path to the test file in the data directory at the project root.
        current_dir = dirname(abspath(__file__))
        project_root = abspath(join(current_dir, ".."))
        self.test_file = join(project_root, "data", "test_mortgage_details.json")
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('builtins.input', side_effect=[
        "500000",  # Home value
        "20%",     # Down payment as percentage
        "30",      # Loan term
        "6.375"    # Interest rate
    ])
    def test_get_mortgage_details(self, mock_inputs):
        details = get_mortgage_details(filename=self.test_file)
        self.assertEqual(details['home_value'], 500000)
        self.assertEqual(details['loan_term'], 30)
        self.assertAlmostEqual(details['interest_rate'], 6.375)
        # The down payment should be 20% of 500,000, i.e., 100,000.
        self.assertAlmostEqual(details['down_payment'], 100000)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
