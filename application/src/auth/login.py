from database.db import get_connection


def login():
    """
    Login to the ATM.

    NOTE:
    This function intentionally contains an SQL Injection vulnerability
    for the laboratory assignment.
    """

    account_no = input("Enter account number: ")
    pin = input("Enter PIN: ")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # INTENTIONALLY VULNERABLE
        # User input is directly inserted into the SQL query.
        query = (
            "SELECT * FROM users "
            f"WHERE account_no = '{account_no}' "
            f"AND pin = '{pin}'"
        )

        cursor.execute(query)

        user = cursor.fetchone()

        if user:
            print("\nLogin successful!")
            print(f"Welcome, {user['name']}!")

            return user

        print("\nInvalid account number or PIN.")
        return None

    finally:
        connection.close()