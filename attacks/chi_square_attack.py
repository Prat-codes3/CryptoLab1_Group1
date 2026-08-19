from shift_cipher import decrypt

ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782,
    'D': 4.253, 'E': 12.702, 'F': 2.228,
    'G': 2.015, 'H': 6.094, 'I': 6.966,
    'J': 0.153, 'K': 0.772, 'L': 4.025,
    'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987,
    'S': 6.327, 'T': 9.056, 'U': 2.758,
    'V': 0.978, 'W': 2.360, 'X': 0.150,
    'Y': 1.974, 'Z': 0.074
}


def chi_square_stat(text):
    text = text.upper()

    total_letters = sum(1 for ch in text if ch.isalpha())

    if total_letters == 0:
        return float('inf')

    chi_square = 0

    for letter in ENGLISH_FREQ:
        observed = text.count(letter)
        expected = total_letters * ENGLISH_FREQ[letter] / 100

        chi_square += ((observed - expected) ** 2) / expected

    return chi_square


def chi_square_attack(ciphertext):
    best_key = 0
    best_plaintext = ""
    min_chi = float('inf')

    for key in range(26):
        plaintext = decrypt(ciphertext, key)

        chi = chi_square_stat(plaintext)

        if chi < min_chi:
            min_chi = chi
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, min_chi