# tests/test_calculator.py

import unittest
from mortgage.calculator import MortgageCalculator

class TestMortgageCalculator(unittest.TestCase):
    def setUp(self):
        # Home Value: $500,000, Down Payment: 20% ($100,000), so Principal = $400,000,
        # Loan Term: 30 years (360 months), Interest Rate: 6.375%
        self.home_value = 500000
        self.down_payment = self.home_value * 0.20  # $100,000
        self.loan_term = 30
        self.interest_rate = 6.375
        self.calculator = MortgageCalculator(
            home_value=self.home_value,
            down_payment=self.down_payment,
            loan_term=self.loan_term,
            interest_rate=self.interest_rate
        )

    def test_monthly_payment(self):
        # Our calculator computes a monthly payment of approximately 2495.48.
        # (Note: Different rounding conventions can lead to small discrepancies.)
        self.assertAlmostEqual(self.calculator.monthly_payment, 2495.48, places=2)

    def test_amortization_schedule_no_prepayments(self):
        schedule = self.calculator.get_amortization_schedule(prepayment_schedule={})
        # Final balance should be effectively 0 and final payment occurs in 360 months.
        final_entry = schedule[-1]
        self.assertAlmostEqual(final_entry["balance"], 0, places=2)
        self.assertEqual(final_entry["month"], 360)

    def test_amortization_schedule_with_prepayments(self):
        # Test with a custom prepayment schedule: extra $5,000 each month.
        prepayment_schedule = {month: 5000 for month in range(1, self.calculator.total_payments + 1)}
        schedule = self.calculator.get_amortization_schedule(prepayment_schedule=prepayment_schedule)
        final_entry = schedule[-1]
        # Loan should be paid off before 360 months.
        self.assertLess(final_entry["month"], 360)
        self.assertAlmostEqual(final_entry["balance"], 0, places=2)

if __name__ == '__main__':
    unittest.main()
