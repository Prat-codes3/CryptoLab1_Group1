import analysis.analyze as analyze
from utils.logger import log_action

def main():
    while True:

        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            log_action("Encrypt")
            print("\nEncrypt: Coming Soon")

        elif choice == "2":
            log_action("Decrypt")
            print("\nDecrypt: Coming Soon")

        elif choice == "3":
            log_action("Attack")
            print("\nAttack: Coming Soon")

        elif choice == "4":
            log_action("Analyze")
            filename = input("Enter the file name: ")
            analyze.analyze_text_file(filename)

        elif choice == "5":
            log_action("Exit")
            print("\nExiting CryptoLabX. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()