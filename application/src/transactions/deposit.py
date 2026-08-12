"""
ATM Deposit

This module handles the Deposit functionality.
It expects an open sqlite3 connection and the account number
of the currently logged-in user.
"""


def deposit(conn, account_no):
    """
    Deposit money into the logged-in user's account.

    Parameters:
        conn: An open sqlite3 database connection.
        account_no: The account number of the logged-in user.

    Returns:
        True if the deposit is successful, otherwise False.
    """
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE account_no = ?",
        (account_no,)
    )

    user = cursor.fetchone()

    if user is None:
        print("\nAccount not found.")
        return False

    current_balance = user[0]

    print("\n===== DEPOSIT =====")
    print(f"Current Balance: ₹{current_balance:.2f}")

    try:
        amount = float(input("Enter deposit amount: ₹"))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return False

    if amount <= 0:
        print("Deposit amount must be greater than zero.")
        return False

    new_balance = current_balance + amount

    cursor.execute(
        "UPDATE users SET balance = ? WHERE account_no = ?",
        (new_balance, account_no)
    )

    conn.commit()

    print("\nDeposit successful.")
    print(f"Deposited Amount: ₹{amount:.2f}")
    print(f"New Balance: ₹{new_balance:.2f}")
    print("===================")

    return True