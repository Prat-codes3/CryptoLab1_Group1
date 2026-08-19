def encrypt(plaintext, key):
    ciphertext = ""

    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            ciphertext += chr((ord(ch) - base + key) % 26 + base)
        else:
            ciphertext += ch

    return ciphertext


def decrypt(ciphertext, key):
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            plaintext += chr((ord(ch) - base - key) % 26 + base)
        else:
            plaintext += ch

    return plaintext