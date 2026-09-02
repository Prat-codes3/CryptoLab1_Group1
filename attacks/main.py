
from shift_cipher import encrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


def main():
    print("===== Shift Cipher Cryptanalysis =====")

    plaintext = input("Enter plaintext: ")
    key = int(input("Enter shift key (0-25): "))

    if key < 0 or key > 25:
        print("Error: Key must be between 0 and 25.")
        return

    ciphertext = encrypt(plaintext, key)

    print("\nCiphertext:", ciphertext)

    dictionary_key, dictionary_plaintext, dictionary_score = dictionary_attack(
        ciphertext,
        "english_words.txt"
    )

    chi_key, chi_plaintext, chi_value = chi_square_attack(ciphertext)

    print("\n===== Dictionary Scoring Attack =====")
    print("Predicted Key:", dictionary_key)
    print("Recovered Plaintext:", dictionary_plaintext)
    print("Dictionary Score:", dictionary_score)

    print("\n===== Chi-Square Attack =====")
    print("Predicted Key:", chi_key)
    print("Recovered Plaintext:", chi_plaintext)
    print("Chi-Square Value:", chi_value)

    print("\n===== Comparison =====")
    print("Actual Key:", key)
    print("Dictionary Key:", dictionary_key)
    print("Chi-Square Key:", chi_key)

    print(
        "Dictionary Correct?",
        "Yes" if dictionary_key == key else "No"
    )

    print(
        "Chi-Square Correct?",
        "Yes" if chi_key == key else "No"
    )


if __name__ == "__main__":
    main()

