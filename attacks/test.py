from shift_cipher import encrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack
import csv
import os

test_cases = [
    ("HELLO WORLD", 3),
    ("THIS IS A TEST", 7),
    ("CRYPTOGRAPHY IS FUN", 10),
    ("COMPUTER SECURITY LAB", 15),
    ("ATTACK AT DAWN", 20),
    ("HI", 5),
    ("CAT", 8),
    ("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", 12),
    ("yoo sup dslkdsj",7)
]

output_file = "../outputs/results.csv"

os.makedirs("../outputs", exist_ok=True)

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Test Case",
        "Actual Key",
        "Dictionary Key",
        "Chi-Square Key",
        "Dictionary Correct?",
        "Chi-Square Correct?"
    ])

    print("-" * 120)
    print(
        f"{'Test Case':35}"
        f"{'Actual Key':12}"
        f"{'Dictionary Key':18}"
        f"{'Chi-Square Key':18}"
        f"{'Dictionary Correct?':20}"
        f"{'Chi-Square Correct?':20}"
    )
    print("-" * 120)

    for plaintext, actual_key in test_cases:

        ciphertext = encrypt(plaintext, actual_key)

        dict_key, _, _ = dictionary_attack(
            ciphertext,
            "english_words.txt"
        )

        chi_key, _, _ = chi_square_attack(ciphertext)

        dict_correct = "Yes" if dict_key == actual_key else "No"
        chi_correct = "Yes" if chi_key == actual_key else "No"

        writer.writerow([
            plaintext,
            actual_key,
            dict_key,
            chi_key,
            dict_correct,
            chi_correct
        ])

        print(
            f"{plaintext[:35]:35}"
            f"{actual_key:<12}"
            f"{dict_key:<18}"
            f"{chi_key:<18}"
            f"{dict_correct:<20}"
            f"{chi_correct:<20}"
        )

print(f"\nResults saved to: {output_file}")