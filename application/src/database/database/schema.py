from application.src.database.database.db import get_connection


def initialize_database():
    """
    Create the users table if it does not already exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                account_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance REAL NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


def seed_users():
    """
    Insert sample ATM accounts if the database is empty.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")

        count = cursor.fetchone()[0]

        if count == 0:

            users = [
                (1001, "Rahul", "1234", 10000.0),
                (1002, "Aman", "5678", 7500.0),
                (1003, "Priya", "4321", 15000.0)
            ]

            cursor.executemany("""
                INSERT INTO users
                (account_no, name, pin, balance)
                VALUES (?, ?, ?, ?)
            """, users)

            connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    seed_users()

    print("Database initialized successfully.")