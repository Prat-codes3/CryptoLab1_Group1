from database.db import update_balance


def withdraw(user):
    """
    Withdraw money from the user's account.


    """

    print(f"\nCurrent balance: ₹{user['balance']:.2f}")

    amount_input = input("Enter withdrawal amount: ")

    try:
        amount = float(amount_input)
    except ValueError:
        print("Invalid amount.")
        return user

    # INTENTIONALLY INSUFFICIENT VALIDATION
    #
    # We only check whether the user has enough balance.
    # We do NOT check whether amount is positive.
    #
    # Therefore a negative amount can cause the balance to increase.
    if amount > user["balance"]:
        print("Insufficient balance.")
        return user

    new_balance = user["balance"] - amount

    update_balance(user["account_no"], new_balance)

    # sqlite3.Row cannot be modified directly,
    # so create a new dictionary-like representation.
    updated_user = dict(user)
    updated_user["balance"] = new_balance

    print(f"\nWithdrawal successful!")
    print(f"Amount: ₹{amount:.2f}")
    print(f"New balance: ₹{new_balance:.2f}")

    return updated_user