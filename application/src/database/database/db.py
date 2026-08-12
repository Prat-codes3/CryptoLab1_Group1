import sqlite3
from pathlib import Path


# Project root = secure_application/
BASE_DIR = Path(__file__).resolve().parents[2]

# Database will be stored in secure_application/data/
DB_PATH = BASE_DIR / "data" / "atm.db"


def get_connection():
    """
    Create and return a connection to the ATM SQLite database.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def get_user(account_no):
    """
    Fetch a user using their account number.
    Returns a Row object or None.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE account_no = ?",
            (account_no,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def update_balance(account_no, new_balance):
    """
    Update the balance of a particular account.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE users SET balance = ? WHERE account_no = ?",
            (new_balance, account_no)
        )

        connection.commit()

    finally:
        connection.close()


def update_pin(account_no, new_pin):
    """
    Update the PIN of a particular account.
    This will be used later by Member 2.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE users SET pin = ? WHERE account_no = ?",
            (new_pin, account_no)
        )

        connection.commit()

    finally:
        connection.close()