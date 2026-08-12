"""
ATM Withdrawal

This module handles the Withdrawal functionality.

NOTE:
This implementation intentionally contains an input-validation
vulnerability for the laboratory assignment.
"""


def withdraw(conn, account_no):
    """
    Withdraw money from the logged-in user's account.

    Parameters:
        conn: An open sqlite3 database connection.
        account_no: The account number of the logged-in user.

    Returns:
        True if the withdrawal is successful, otherwise False.
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

    print("\nWITHDRAW")
    print(f"Current Balance: ₹{current_balance:.2f}")

    try:
        amount = float(input("Enter withdrawal amount: ₹"))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return False

    # INTENTIONALLY VULNERABLE:
    # Negative withdrawal amounts are not rejected.
    if amount > current_balance:
        print("Insufficient balance.")
        return False

    new_balance = current_balance - amount

    cursor.execute(
        "UPDATE users SET balance = ? WHERE account_no = ?",
        (new_balance, account_no)
    )

    conn.commit()

    print("\nWithdrawal successful.")
    print(f"Withdrawn Amount: ₹{amount:.2f}")
    print(f"New Balance: ₹{new_balance:.2f}")
    print("\n")

    return True