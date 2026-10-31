"""
Simple ATM System (beginner friendly)
-------------------------------------
Features:
  - PIN login (3 attempts, then the card is locked)
  - Check balance, deposit, withdraw, change PIN, view history
  - Checks every input for mistakes (letters, negatives, empty input, etc.)

How to run:   python atm.py
Demo cards:   Card 1001 / PIN 1234    Card 1002 / PIN 4321
"""

MAX_ATTEMPTS = 3          # wrong PIN tries allowed
DAILY_LIMIT = 500.00      # max total withdrawal per session

# Our tiny "bank database". Key = card number.
accounts = {
    "1001": {"name": "Ada",  "pin": "1234", "balance": 1000.00, "history": [], "locked": False},
    "1002": {"name": "Tunde", "pin": "4321", "balance": 250.50, "history": [], "locked": False},
}


# ---------- Helper functions (safe input) ----------

def ask_amount(prompt):
    """Ask for a money amount. Keeps asking until the input is valid.
    Returns a positive number with at most 2 decimals, or None if user types 'c' to cancel."""
    while True:
        text = input(prompt).strip()

        if text.lower() == "c":
            return None
        if text == "":
            print("  Error: you typed nothing. Try again (or 'c' to cancel).")
            continue

        try:
            amount = float(text)
        except ValueError:
            print("  Error: please enter numbers only, like 50 or 20.75.")
            continue

        if amount != amount or amount in (float("inf"), float("-inf")):
            print("  Error: that is not a real amount.")
            continue
        if amount <= 0:
            print("  Error: amount must be greater than zero.")
            continue
        if round(amount, 2) != amount:
            print("  Error: use at most 2 decimal places.")
            continue

        return amount


def valid_pin_format(pin):
    """A PIN must be exactly 4 digits."""
    return len(pin) == 4 and pin.isdigit()


def record(account, text):
    """Save a line in the account history."""
    account["history"].append(text)


# ---------- ATM actions ----------

def check_balance(account):
    print(f"\n  Your balance is: ${account['balance']:.2f}")


def deposit(account):
    amount = ask_amount("\n  Amount to deposit (or 'c' to cancel): $")
    if amount is None:
        print("  Cancelled.")
        return
    account["balance"] = round(account["balance"] + amount, 2)
    record(account, f"Deposit   +${amount:.2f}")
    print(f"  Deposited ${amount:.2f}. New balance: ${account['balance']:.2f}")


def withdraw(account, withdrawn_so_far):
    """Returns the new total withdrawn this session."""
    amount = ask_amount("\n  Amount to withdraw (or 'c' to cancel): $")
    if amount is None:
        print("  Cancelled.")
        return withdrawn_so_far

    if amount > account["balance"]:
        print(f"  Error: not enough money. Your balance is ${account['balance']:.2f}.")
        return withdrawn_so_far
    if withdrawn_so_far + amount > DAILY_LIMIT:
        left = DAILY_LIMIT - withdrawn_so_far
        print(f"  Error: session limit is ${DAILY_LIMIT:.2f}. You can still withdraw ${left:.2f}.")
        return withdrawn_so_far

    account["balance"] = round(account["balance"] - amount, 2)
    record(account, f"Withdraw  -${amount:.2f}")
    print(f"  Please take your cash: ${amount:.2f}. New balance: ${account['balance']:.2f}")
    return withdrawn_so_far + amount


def change_pin(account):
    old = input("\n  Enter your CURRENT PIN: ").strip()
    if old != account["pin"]:
        print("  Error: wrong current PIN.")
        return

    new = input("  Enter NEW 4-digit PIN: ").strip()
    if not valid_pin_format(new):
        print("  Error: PIN must be exactly 4 digits (numbers only).")
        return
    if new == account["pin"]:
        print("  Error: new PIN must be different from the old one.")
        return

    again = input("  Enter NEW PIN again to confirm: ").strip()
    if again != new:
        print("  Error: the two PINs do not match. PIN not changed.")
        return

    account["pin"] = new
    record(account, "PIN changed")
    print("  PIN changed successfully.")


def show_history(account):
    print("\n  --- Transaction history ---")
    if not account["history"]:
        print("  (no transactions yet)")
    for line in account["history"]:
        print("  " + line)


# ---------- Login ----------

def login():
    """Returns the account if login works, otherwise None."""
    card = input("Enter your card number: ").strip()

    if card not in accounts:
        print("Error: card not found.")
        return None

    account = accounts[card]
    if account["locked"]:
        print("This card is LOCKED. Please contact your bank.")
        return None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        pin = input("Enter your 4-digit PIN: ").strip()

        if not valid_pin_format(pin):
            print("  PIN must be 4 digits.")
        elif pin == account["pin"]:
            print(f"\nWelcome, {account['name']}!")
            return account
        else:
            print("  Wrong PIN.")

        left = MAX_ATTEMPTS - attempt
        if left > 0:
            print(f"  Attempts left: {left}")

    account["locked"] = True
    print("Too many wrong attempts. Card LOCKED.")
    return None


# ---------- Main program ----------

def menu(account):
    withdrawn = 0.0
    while True:
        print("\n========== ATM MENU ==========")
        print("  1. Check balance")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Change PIN")
        print("  5. Transaction history")
        print("  6. Exit")
        choice = input("Choose 1-6: ").strip()

        if choice == "1":
            check_balance(account)
        elif choice == "2":
            deposit(account)
        elif choice == "3":
            withdrawn = withdraw(account, withdrawn)
        elif choice == "4":
            change_pin(account)
        elif choice == "5":
            show_history(account)
        elif choice == "6":
            print("\nThank you for using our ATM. Goodbye!")
            return
        else:
            print("  Error: please type a number from 1 to 6.")


def main():
    print("===== WELCOME TO PYTHON BANK ATM =====")
    while True:
        account = login()
        if account:
            menu(account)
        again = input("\nStart a new session? (y/n): ").strip().lower()
        if again != "y":
            print("Machine shutting down.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSession ended. Goodbye!")