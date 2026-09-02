
from shift_cipher import decrypt
import os


def load_dictionary(filename):
    dictionary = set()

    # Find the directory where this Python file is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the full path to the dictionary
    dictionary_path = os.path.join(current_directory, filename)

    with open(dictionary_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                dictionary.add(word)

    return dictionary


def dictionary_attack(ciphertext, dictionary_file):
    dictionary = load_dictionary(dictionary_file)

    best_key = 0
    best_score = -1
    best_plaintext = ""

    # Try all 26 possible keys
    for key in range(26):

        # Decrypt using the current key
        plaintext = decrypt(ciphertext, key)

        # Split plaintext into words
        words = plaintext.lower().split()

        score = 0

        # Compare words with the dictionary
        for word in words:

            # Remove punctuation
            word = word.strip(".,!?;:\"'()[]{}")

            if word in dictionary:
                score += 1

        # Keep the key with the highest score
        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score

