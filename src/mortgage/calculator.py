# src/mortgage/calculator.py

class MortgageCalculator:
    def __init__(self, home_value: float, down_payment: float, loan_term: int, interest_rate: float):
        """
        Initialize the mortgage calculator with the given parameters.

        :param home_value: The value of the home in dollars.
        :param down_payment: The down payment in dollars.
        :param loan_term: The loan term in years (commonly 10, 15, or 30).
        :param interest_rate: The annual interest rate as a percentage (e.g., 4.5 for 4.5%).
        """
        self.home_value = home_value
        self.down_payment = down_payment
        self.loan_term = loan_term
        self.interest_rate = interest_rate

        # Calculate common loan parameters once
        self.principal = self.home_value - self.down_payment
        self.monthly_rate = self.interest_rate / 100 / 12
        self.total_payments = self.loan_term * 12
        self.monthly_payment = self._calculate_monthly_payment()

    def _calculate_monthly_payment(self) -> float:
        """Private method to calculate the standard monthly payment (without prepayments)."""
        if self.monthly_rate != 0:
            return self.principal * (self.monthly_rate * (1 + self.monthly_rate) ** self.total_payments) / (
                    (1 + self.monthly_rate) ** self.total_payments - 1)
        else:
            return self.principal / self.total_payments

    def get_amortization_schedule(self, prepayment_schedule: dict = None) -> list:
        """
        Compute the full amortization schedule.

        :param prepayment_schedule: Optional dict mapping month numbers to extra prepayment amounts.
        :return: A list of dictionaries; each represents a month's details (payment, interest, principal, extra, balance).
        """
        schedule = []
        current_balance = self.principal
        month = 1

        while month <= self.total_payments and current_balance > 0:
            # Determine extra payment if scheduled for this month.
            extra_payment = prepayment_schedule.get(month, 0) if prepayment_schedule else 0

            # Apply the extra payment at the start of the month.
            if extra_payment:
                current_balance -= extra_payment
                if current_balance < 0:
                    extra_payment += current_balance  # Adjust extra if overpaid.
                    current_balance = 0

            # Regular monthly payment calculations.
            interest_payment = current_balance * self.monthly_rate
            principal_payment = self.monthly_payment - interest_payment

            # If the remaining balance is less than the computed principal payment, adjust.
            if principal_payment > current_balance:
                principal_payment = current_balance
                self.monthly_payment = principal_payment + interest_payment

            current_balance -= principal_payment
            if current_balance < 0:
                current_balance = 0

            schedule.append({
                "month": month,
                "payment": self.monthly_payment,
                "principal_payment": principal_payment,
                "interest_payment": interest_payment,
                "extra_payment": extra_payment,
                "balance": current_balance
            })
            month += 1

        return schedule

    def print_summary(self):
        """Print a summary of the mortgage parameters and key calculated values."""
        print("Mortgage Summary:")
        print(f"Home Value: ${self.home_value:,.2f}")
        print(f"Down Payment: ${self.down_payment:,.2f}")
        print(f"Loan Term: {self.loan_term} years")
        print(f"Interest Rate: {self.interest_rate:.2f}%")
        print(f"Principal: ${self.principal:,.2f}")
        print(f"Monthly Payment: ${self.monthly_payment:,.2f}")
        print(f"Total Payments (months): {self.total_payments}")

    def print_schedule(self, prepayment_schedule: dict = None):
        """
        Print the full amortization schedule.

        :param prepayment_schedule: Optional dict mapping month numbers to extra prepayment amounts.
        """
        schedule = self.get_amortization_schedule(prepayment_schedule)
        print("Month |   Payment   |  Principal  |   Interest  | Extra Payment |   Balance")
        print("-" * 80)
        for entry in schedule:
            print(f"{entry['month']:5d} | {entry['payment']:11.2f} | {entry['principal_payment']:11.2f} | "
                  f"{entry['interest_payment']:11.2f} | {entry['extra_payment']:13.2f} | {entry['balance']:11.2f}")
