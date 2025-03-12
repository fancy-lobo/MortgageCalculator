class MortgageCalculator:
    def __init__(self, home_value: float, down_payment: float, loan_term: int, interest_rate: float):
        self.home_value = home_value
        self.down_payment = down_payment
        self.loan_term = loan_term
        self.interest_rate = interest_rate

        # Calculate common loan parameters once.
        self.principal = self.home_value - self.down_payment
        self.monthly_rate = self.interest_rate / 100 / 12
        self.total_payments = self.loan_term * 12
        self.monthly_payment = self._calculate_monthly_payment()

    def _calculate_monthly_payment(self) -> float:
        if self.monthly_rate != 0:
            return self.principal * (self.monthly_rate * (1 + self.monthly_rate) ** self.total_payments) / (
                    (1 + self.monthly_rate) ** self.total_payments - 1)
        else:
            return self.principal / self.total_payments

    def get_amortization_schedule(self, prepayment_schedule: dict = None) -> list:
        schedule = []
        current_balance = self.principal
        month = 1
        # Use a local copy so that self.monthly_payment remains unchanged.
        monthly_payment = self.monthly_payment

        while month <= self.total_payments and current_balance > 0:
            # Apply extra payment if scheduled for this month.
            extra_payment = prepayment_schedule.get(month, 0) if prepayment_schedule else 0
            if extra_payment:
                current_balance -= extra_payment
                if current_balance < 0:
                    extra_payment += current_balance  # Adjust for overpayment.
                    current_balance = 0

            interest_payment = current_balance * self.monthly_rate
            principal_payment = monthly_payment - interest_payment

            # Adjust if the remaining balance is less than the computed principal payment.
            if principal_payment > current_balance:
                principal_payment = current_balance
                monthly_payment = principal_payment + interest_payment

            current_balance -= principal_payment
            if current_balance < 0:
                current_balance = 0

            schedule.append({
                "month": month,
                "payment": monthly_payment,
                "principal_payment": principal_payment,
                "interest_payment": interest_payment,
                "extra_payment": extra_payment,
                "balance": current_balance
            })
            month += 1

        return schedule

    def print_schedule(self, prepayment_schedule: dict = None):
        schedule = self.get_amortization_schedule(prepayment_schedule)
        print("Month |   Payment   |  Principal  |   Interest  | Extra Payment |   Balance")
        print("-" * 80)
        for entry in schedule:
            print(f"{entry['month']:5d} | {entry['payment']:11.2f} | {entry['principal_payment']:11.2f} | "
                  f"{entry['interest_payment']:11.2f} | {entry['extra_payment']:13.2f} | {entry['balance']:11.2f}")

    def print_updated_summary(self, prepayment_schedule: dict = None):
        """
        Compute and print an updated summary based on the amortization schedule
        that factors in any prepayment inputs. This summary now includes the total
        interest paid as a percentage of both the principal and the home value.
        """
        schedule = self.get_amortization_schedule(prepayment_schedule)
        if schedule:
            total_interest = sum(item['interest_payment'] for item in schedule)
            final_month = schedule[-1]['month']

            # Convert final_month into years and months.
            if final_month >= 12:
                years = final_month // 12
                months = final_month % 12
                if months > 0:
                    payoff_time = f"{years} year(s) and {months} month(s)"
                else:
                    payoff_time = f"{years} year(s)"
            else:
                payoff_time = f"{final_month} month(s)"

            # Calculate interest as a percentage of principal and home value.
            interest_percent_principal = (total_interest / self.principal) * 100
            interest_percent_home_value = (total_interest / self.home_value) * 100

            print("\nUpdated Mortgage Summary with Prepayments:")
            print(f"Loan is paid off in {payoff_time}.")
            print(f"Total interest paid: ${total_interest:,.2f}")
            print(f"Interest as percentage of principal: {interest_percent_principal:.2f}%")
            print(f"Interest as percentage of home value: {interest_percent_home_value:.2f}%")
        else:
            print("No payment schedule available.")

    def print_summary(self):
        """
        Print the base mortgage summary based on the input parameters only.
        (This doesn't factor in prepayments.)
        """
        print("Mortgage Summary:")
        print(f"Home Value: ${self.home_value:,.2f}")
        print(f"Down Payment: ${self.down_payment:,.2f}")
        print(f"Loan Term: {self.loan_term} years")
        print(f"Interest Rate: {self.interest_rate:.2f}%")
        print(f"Principal: ${self.principal:,.2f}")
        print(f"Monthly Payment (without prepayments): ${self.monthly_payment:,.2f}")
        print(f"Total Payments (months): {self.total_payments}")
