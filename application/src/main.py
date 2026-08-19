# from database.schema import initialize_database, seed_users
# from auth.login import login

# from transactions.balance import check_balance
# from transactions.withdraw import withdraw
# from transactions.deposit import deposit

# from account.pin_change import change_pin


# def atm_menu(user):
#     """
#     Display the ATM menu after successful login.
#     """

#     while True:
#         print("\n" + "=" * 30)
#         print("          ATM MENU")
#         print("=" * 30)
#         print("1. Balance Inquiry")
#         print("2. Withdraw")
#         print("3. Deposit")
#         print("4. Change PIN")
#         print("5. Logout")
#         print("=" * 30)

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             user = check_balance(user)

#         elif choice == "2":
#             user = withdraw(user)

#         elif choice == "3":
#             user = deposit(user)

#         elif choice == "4":
#             user = change_pin(user)

#         elif choice == "5":
#             print("\nLogged out successfully.")
#             break

#         else:
#             print("\nInvalid choice. Please try again.")


# def main():
#     """
#     Main entry point of the ATM application.
#     """

#     # Create database and sample users if required
#     initialize_database()
#     seed_users()

#     while True:
#         print("\n" + "=" * 30)
#         print("       WELCOME TO ATM")
#         print("=" * 30)
#         print("1. Login")
#         print("2. Exit")
#         print("=" * 30)

#         choice = input("Enter your choice: ")

#         if choice == "1":

#             user = login()

#             if user:
#                 atm_menu(user)

#         elif choice == "2":
#             print("\nThank you for using the ATM.")
#             break

#         else:
#             print("\nInvalid choice. Please try again.")


# if __name__ == "__main__":
#     main()












# from database.schema import initialize_database, seed_users
# from auth.login import login
# from transactions.balance import balance_inquiry
# from transactions.deposit import deposit
# from transactions.withdraw import withdraw
# from account.pin_change import change_pin

# def atm_menu(user):
#     while True:
#         print("\n===== ATM MENU =====")
#         print("1. Balance Inquiry")
#         print("2. Withdraw")
#         print("3. Deposit")
#         print("4. Logout")

#         choice = input("Enter choice: ")

#         if choice == "1":
#             balance_inquiry(user)

#         elif choice == "2":
#             withdraw(user)

#         elif choice == "3":
#             deposit(user)

#         elif choice == "4":
#             print("Logged out successfully.")
#             break

#         else:
#             print("Invalid choice")


# def main():
#     while True:
#         print("\n===== ATM SYSTEM =====")
#         print("1. Login")
#         print("2. Exit")

#         choice = input("Enter choice: ")

#         if choice == "1":
#             user = login()

#             if user:
#                 atm_menu(user)

#         elif choice == "2":
#             print("Thank you for using ATM.")
#             break

#         else:
#             print("Invalid choice")


# if __name__ == "__main__":
#     main()


from auth.login import login

from transactions.balance import show_balance
from transactions.withdraw import withdraw
from transactions.deposit import deposit


def atm_menu(user):
    while True:
        print("\n===== ATM MENU =====")
        print("1. Balance Inquiry")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            show_balance(user["account_no"])

        elif choice == "2":
            withdraw(user["account_no"])

        elif choice == "3":
            deposit(user["account_no"])

        elif choice == "4":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice.")


def main():
    while True:
        print("\n===== ATM SYSTEM =====")
        print("1. Login")
        print("2. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            user = login()

            if user:
                atm_menu(user)

        elif choice == "2":
            print("\nThank you for using ATM.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()