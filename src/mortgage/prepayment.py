# src/mortgage/prepayment.py

def get_prepayment_schedule() -> dict:
    """
    Ask the user whether they want to include prepayments, then allow them to specify:
      - Whether all prepayments are equal or custom per interval.
      - When prepayments start (month number), frequency (in months), and number of intervals.
    Returns:
      A dictionary mapping month numbers to prepayment amounts.
    """
    prepay_choice = input("Do you want to add prepayments? (y/yes to include): ").strip().lower()
    if prepay_choice not in ['y', 'yes']:
        return {}

    # Ask whether the prepayments will be equal or custom.
    equal_choice = input("Should all prepayments be equal? (y/yes for equal, otherwise custom): ").strip().lower()

    # Ask for the start month, frequency, and number of intervals.
    start_month = int(input("Enter the month number when prepayments should begin (e.g., 1 for the first month): "))
    frequency_months = int(input("Enter the frequency (in months) for prepayments (e.g., 12 for yearly): "))
    num_intervals = int(input("Enter the number of prepayment intervals: "))

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
