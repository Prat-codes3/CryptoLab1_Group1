"""
ATM Balance Inquiry

This module handles the Balance Inquiry functionality.
It expects the main application/database layer to provide an
already-open SQLite connection.
"""

# def show_balance(conn, account_no):
#     """
#     Display the account holder's name, account number, and balance.

#     Parameters:
#         conn: An open sqlite3 database connection.
#         account_no: The account number of the logged-in user.

#     Returns:
#         True if the account was found, otherwise False.
#     """
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT account_no, name, balance FROM users WHERE account_no = ?",
#         (account_no,)
#     )

#     user = cursor.fetchone()

#     if user is None:
#         print("\nAccount not found.")
#         return False

#     account, name, balance = user

#     print("\n")
#     print(f"Account Number : {account}")
#     print(f"Account Holder : {name}")
#     print(f"Current Balance: ₹{balance:.2f}")
#     print("\n")

#     return True


from database.db import get_connection


def show_balance(account_no):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT account_no, name, balance FROM users WHERE account_no = ?",
            (account_no,)
        )

        user = cursor.fetchone()

        if user is None:
            print("\nAccount not found.")
            return False

        print("\n===== ACCOUNT DETAILS =====")
        print(f"Account Number : {user['account_no']}")
        print(f"Account Holder : {user['name']}")
        print(f"Current Balance: ₹{user['balance']:.2f}")

        return True

    finally:
        conn.close()