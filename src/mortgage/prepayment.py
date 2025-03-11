# src/mortgage/prepayment.py

import os
import json


def get_project_root() -> str:
    """
    Returns the absolute path of the project root directory.
    Assumes this file is located at project_root/src/mortgage/prepayment.py.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return project_root


def get_prepayment_schedule(total_payments: int = None, filename: str = None) -> dict:
    """
    Check if saved prepayment details exist in the data directory at the project root.
    If found, ask the user if they want to reuse them.
    Otherwise, prompt for new prepayment details.

    The user can specify:
      - Whether all prepayments are equal or custom,
      - The start month,
      - The frequency (in months),
      - The number of intervals, or an option to prepay indefinitely.

    When 'indefinitely' is chosen and total_payments is provided, the number of intervals is calculated as:
      num_intervals = ((total_payments - start_month) // frequency_months) + 1

    Returns:
      A dictionary mapping month numbers (as integers) to prepayment amounts.
    """
    if filename is None:
        project_root = get_project_root()
        filename = os.path.join(project_root, "data", "prepayment_details.json")

    # Ensure the data directory exists.
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Check for existing prepayment details.
    if os.path.exists(filename):
        reuse = input("Found saved prepayment details. Do you want to use them? (y/yes to reuse): ").strip().lower()
        if reuse in ['y', 'yes']:
            with open(filename, "r") as f:
                saved_details = json.load(f)
            # Convert keys back to integers.
            saved_details = {int(k): v for k, v in saved_details.items()}
            print("Using saved prepayment details:")
            print(saved_details)
            return saved_details

    # Prompt for new prepayment details.
    equal_choice = input("Should all prepayments be equal? (y/yes for equal, otherwise custom): ").strip().lower()
    start_month = int(input("Enter the month number when prepayments should begin (e.g., 1 for the first month): "))
    frequency_months = int(input("Enter the frequency (in months) for prepayments (e.g., 12 for yearly): "))

    num_intervals_input = input(
        "Enter the number of prepayment intervals (or type 'i' for indefinitely until loan is paid off): "
    ).strip()

    if num_intervals_input.lower() in ['i', 'indefinitely']:
        if total_payments is not None:
            num_intervals = ((total_payments - start_month) // frequency_months) + 1
            print(f"Prepayments will be applied indefinitely for a total of {num_intervals} intervals.")
        else:
            print("Total payments not provided; please enter a number of intervals.")
            num_intervals = int(input("Enter the number of prepayment intervals: "))
    else:
        num_intervals = int(num_intervals_input)

    prepayment_schedule = {}
    if equal_choice in ['y', 'yes']:
        lump_sum = float(input("Enter the lump sum prepayment amount for each interval: "))
        for i in range(num_intervals):
            month = start_month + i * frequency_months
            prepayment_schedule[month] = lump_sum
    else:
        for i in range(num_intervals):
            month = start_month + i * frequency_months
            amount = float(input(f"Enter the prepayment amount for month {month}: "))
            prepayment_schedule[month] = amount

    # Save the new prepayment details to the file.
    with open(filename, "w") as f:
        json.dump(prepayment_schedule, f)

    return prepayment_schedule


def get_prepayment_amount(mortgage_details: dict):
    """
    Determines the required extra prepayment amount (assumed equal at every interval)
    to pay off the loan in a user-specified time.

    The function prompts the user for:
      - The desired payoff time in years.
      - Prepayment frequency (in months).
      - The start month for prepayments.

    It then simulates the loan's amortization schedule with an extra payment X at the scheduled intervals,
    and uses a binary search to compute the extra payment amount required to achieve a zero or near-zero balance
    by the target payoff time.

    Returns:
      A tuple (extra_payment, prepayment_schedule), where extra_payment is the required extra payment per interval,
      and prepayment_schedule is a dictionary mapping the scheduled month numbers to that extra payment amount.
    """
    # Unpack mortgage details.
    home_value = mortgage_details['home_value']
    down_payment = mortgage_details['down_payment']
    principal = home_value - down_payment
    loan_term = mortgage_details['loan_term']
    annual_interest_rate = mortgage_details['interest_rate']
    monthly_rate = annual_interest_rate / 100 / 12
    total_payments = loan_term * 12

    # Calculate the standard monthly payment.
    if monthly_rate != 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / (
                (1 + monthly_rate) ** total_payments - 1)
    else:
        monthly_payment = principal / total_payments

    # Get desired payoff time and prepayment schedule parameters.
    desired_payoff_years = float(input("Enter the desired payoff time with prepayments (in years): "))
    target_months = int(desired_payoff_years * 12)
    frequency_months = int(input("Enter the frequency (in months) for prepayments (e.g., 12 for yearly): "))
    start_month = int(input("Enter the month number when prepayments should begin (e.g., 1 for the first month): "))

    def simulate_with_extra(X: float) -> float:
        """
        Simulate the amortization schedule applying an extra payment X at the scheduled intervals,
        and return the final balance after target_months.
        """
        balance = principal
        month = 1
        while month <= target_months and balance > 0:
            # If this is a prepayment month, apply the extra payment.
            if month >= start_month and ((month - start_month) % frequency_months == 0):
                balance -= X
                if balance <= 0:
                    return balance
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            if principal_payment > balance:
                principal_payment = balance
            balance -= principal_payment
            month += 1
        return balance

    # Use binary search to determine the required extra payment X.
    low = 0.0
    high = principal  # Upper bound for extra payment.
    tolerance = 1e-2  # Acceptable tolerance in dollars.
    extra_payment = 0.0

    while low <= high:
        mid = (low + high) / 2
        final_balance = simulate_with_extra(mid)
        if abs(final_balance) < tolerance:
            extra_payment = mid
            break
        elif final_balance > 0:
            # Loan is not paid off; need a higher extra payment.
            low = mid + tolerance
        else:
            high = mid - tolerance

    # Build the prepayment schedule using the computed extra payment.
    num_intervals = ((target_months - start_month) // frequency_months) + 1 if target_months >= start_month else 0
    prepayment_schedule = {}
    for i in range(num_intervals):
        month = start_month + i * frequency_months
        prepayment_schedule[month] = extra_payment

    print(
        f"\nTo pay off the loan in {desired_payoff_years} years, you need to prepay ${extra_payment:,.2f} every {frequency_months} month(s) starting at month {start_month}.")
    return extra_payment, prepayment_schedule
