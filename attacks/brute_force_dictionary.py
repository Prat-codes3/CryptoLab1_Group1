from shift_cipher import decrypt


def load_dictionary(filename):
    dictionary = set()

    with open(filename, "r", encoding="utf-8") as file:
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

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        words = plaintext.lower().split()

        score = 0

        for word in words:

            word = word.strip(".,!?;:\"'()[]{}")

            if word in dictionary:
                score += 1

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score