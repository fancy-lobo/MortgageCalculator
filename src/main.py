# src/main.py

from mortgage.calculator import MortgageCalculator
from utils.mortgage_details import get_mortgage_details
from mortgage.prepayment import get_prepayment_schedule, get_prepayment_amount


def main():
    # Retrieve mortgage details (using persisted data if available)
    details = get_mortgage_details()

    # Create a MortgageCalculator instance.
    calculator = MortgageCalculator(
        home_value=details['home_value'],
        down_payment=details['down_payment'],
        loan_term=details['loan_term'],
        interest_rate=details['interest_rate']
    )

    # Prompt user with numbered options for prepayments.
    prepayment_option = input(
        "\nWould you like to add prepayments? Please select one of the following options:\n"
        "1. Enter a custom prepayment schedule.\n"
        "2. Calculate required prepayment to meet a target payoff time.\n"
        "3. Skip prepayment details.\n"
        "Enter 1, 2, or 3: "
    ).strip()

    if prepayment_option == "1":
        prepayment_schedule = get_prepayment_schedule()
    elif prepayment_option == "2":
        # get_prepayment_amount returns a tuple (extra_payment, prepayment_schedule)
        _, prepayment_schedule = get_prepayment_amount(details)
    else:
        prepayment_schedule = {}

    # Ask if the user wants to view the full amortization schedule.
    show_schedule = input(
        "\nWould you like to see the full amortization schedule? (y/yes to display): ").strip().lower()
    if show_schedule in ['y', 'yes']:
        calculator.print_schedule(prepayment_schedule)

    # Now display the updated mortgage summary reflecting prepayment inputs.
    calculator.print_updated_summary(prepayment_schedule)


if __name__ == "__main__":
    main()
