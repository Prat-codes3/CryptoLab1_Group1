"""
ATM PIN Change

This module handles changing the PIN of the currently
logged-in ATM user.
"""


def change_pin(conn, account_no):
    """
    Change the PIN for the logged-in user.

    Parameters:
        conn: An open sqlite3 database connection.
        account_no: The account number of the logged-in user.

    Returns:
        True if the PIN is changed successfully, otherwise False.
    """

    cursor = conn.cursor()

    cursor.execute(
        "SELECT pin FROM users WHERE account_no = ?",
        (account_no,)
    )

    user = cursor.fetchone()

    if user is None:
        print("\nAccount not found.")
        return False

    current_pin = user[0]

    print("\nCHANGE PIN")

    old_pin = input("Enter current PIN: ")

    if old_pin != current_pin:
        print("Incorrect current PIN.")
        return False

    new_pin = input("Enter new PIN: ")
    confirm_pin = input("Confirm new PIN: ")

    if new_pin != confirm_pin:
        print("New PINs do not match.")
        return False

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return False

    cursor.execute(
        "UPDATE users SET pin = ? WHERE account_no = ?",
        (new_pin, account_no)
    )

    conn.commit()

    print("\nPIN changed successfully.")
    print("\n")

    return True