# src/main.py

from utils.mortgage_details import get_mortgage_details
from mortgage.calculator import MortgageCalculator


def main():
    # Retrieve mortgage details (using persisted data if available)
    details = get_mortgage_details()

    # Create a MortgageCalculator instance with the retrieved details.
    calculator = MortgageCalculator(
        home_value=details['home_value'],
        down_payment=details['down_payment'],
        loan_term=details['loan_term'],
        interest_rate=details['interest_rate']
    )

    # Print a summary of the mortgage parameters.
    calculator.print_summary()

    # Ask the user if they want to view the full amortization schedule.
    show_schedule = input(
        "\nWould you like to see the full amortization schedule? (y/yes to display): ").strip().lower()
    if show_schedule in ['y', 'yes']:
        # Optionally, you could let the user define a prepayment schedule here.
        # For now, we'll use a default schedule if any exists.
        prepayment_schedule = {1: 50000, 13: 50000, 25: 50000, 37: 50000, 49: 50000}
        calculator.print_schedule(prepayment_schedule)
    else:
        print("Amortization schedule display skipped.")


if __name__ == "__main__":
    main()
