import json
import os


def get_mortgage_details(filename="data/mortgage_details.json"):
    """
    Load mortgage details from the specified file if available;
    otherwise prompt for details and save them.
    """
    # Determine the current file's directory (this is in src/utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming the project structure:
    # project_root/
    #   data/
    #   src/
    #     utils/
    # We need to go up two levels to reach the project root.
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    file_path = os.path.join(project_root, filename)

    if os.path.exists(file_path):
        use_saved = input(
            "Found saved mortgage details. Would you like to use them? (y/yes to use saved details): ").strip().lower()
        if use_saved in ['y', 'yes']:
            with open(file_path, "r") as file:
                details = json.load(file)
            print("Using saved mortgage details:")
            print(details)
            return details

    # Otherwise, prompt for new details.
    home_value = float(input("Enter the home value (in dollars): "))

    down_payment_input = input(
        "Enter the down payment (percentage e.g., '20%' or dollar amount e.g., '40000'): ").strip()
    if "%" in down_payment_input:
        down_payment = home_value * (float(down_payment_input.strip('%')) / 100)
    else:
        down_payment = float(down_payment_input.strip('$'))

    while True:
        loan_term = int(input("Enter the loan term in years (10, 15, or 30): "))
        if loan_term in [10, 15, 30]:
            break
        else:
            print("Please enter a valid loan term (10, 15, or 30).")

    interest_rate = float(input("Enter the annual interest rate (as a percentage, e.g., 4.5): "))

    details = {
        'home_value': home_value,
        'down_payment': down_payment,
        'loan_term': loan_term,
        'interest_rate': interest_rate
    }

    # Ensure the data directory exists before saving.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        json.dump(details, file)

    print("Mortgage details saved.")
    return details
