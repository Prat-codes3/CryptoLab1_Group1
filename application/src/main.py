from database.schema import initialize_database, seed_users
from auth.login import login

from transactions.balance import check_balance
from transactions.withdraw import withdraw
from transactions.deposit import deposit

from account.pin_change import change_pin


def atm_menu(user):
    """
    Display the ATM menu after successful login.
    """

    while True:
        print("\n" + "=" * 30)
        print("          ATM MENU")
        print("=" * 30)
        print("1. Balance Inquiry")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Change PIN")
        print("5. Logout")
        print("=" * 30)

        choice = input("Enter your choice: ")

        if choice == "1":
            user = check_balance(user)

        elif choice == "2":
            user = withdraw(user)

        elif choice == "3":
            user = deposit(user)

        elif choice == "4":
            user = change_pin(user)

        elif choice == "5":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice. Please try again.")


def main():
    """
    Main entry point of the ATM application.
    """

    # Create database and sample users if required
    initialize_database()
    seed_users()

    while True:
        print("\n" + "=" * 30)
        print("       WELCOME TO ATM")
        print("=" * 30)
        print("1. Login")
        print("2. Exit")
        print("=" * 30)

        choice = input("Enter your choice: ")

        if choice == "1":

            user = login()

            if user:
                atm_menu(user)

        elif choice == "2":
            print("\nThank you for using the ATM.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()