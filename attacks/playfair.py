from collections import Counter


def generate_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    key = ""
    for ch in keyword:
        if ch in alphabet and ch not in key:
            key += ch

    for ch in alphabet:
        if ch not in key:
            key += ch

    matrix = []
    for i in range(0, 25, 5):
        matrix.append(list(key[i:i + 5]))

    return matrix


def prepare_plaintext(plaintext):
    plaintext = plaintext.upper().replace("J", "I")

    plaintext = ''.join(ch for ch in plaintext if ch.isalpha())

    return plaintext


def create_digraphs(plaintext):
    digraphs = []
    i = 0

    while i < len(plaintext):
        first = plaintext[i]

        if i + 1 >= len(plaintext):
            second = 'X'
            i += 1

        else:
            second = plaintext[i + 1]

            if first == second:
                second = 'X'
                i += 1
            else:
                i += 2

        digraphs.append(first + second)

    return digraphs


def find_position(matrix, ch):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col


def playfair_encrypt(digraphs, matrix):
    ciphertext = ""

    for pair in digraphs:
        a, b = pair[0], pair[1]

        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5]
            ciphertext += matrix[r2][(c2 + 1) % 5]

        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1]
            ciphertext += matrix[(r2 + 1) % 5][c2]

        else:
            ciphertext += matrix[r1][c2]
            ciphertext += matrix[r2][c1]

    return ciphertext


def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i + 1]

        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5]
            plaintext += matrix[r2][(c2 - 1) % 5]

        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1]
            plaintext += matrix[(r2 - 1) % 5][c2]

        else:
            plaintext += matrix[r1][c2]
            plaintext += matrix[r2][c1]

    return plaintext


def digraph_frequency(ciphertext):
    frequencies = Counter()

    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i + 2]
        frequencies[digraph] += 1

    return frequencies


def verify(original_plaintext, decrypted_plaintext, matrix):
    prepared = prepare_plaintext(original_plaintext)

    expected_digraphs = create_digraphs(prepared)
    expected = ''.join(expected_digraphs)

    if expected == decrypted_plaintext:
        return "SUCCESS"
    else:
        return "FAILED"


keyword = "MONARCHY"
plaintext = "INSTRUMENTS"

matrix = generate_key_matrix(keyword)

print("Key Matrix")
for row in matrix:
    print(" ".join(row))

prepared = prepare_plaintext(plaintext)

digraphs = create_digraphs(prepared)

print("\nPrepared Digraphs:")
print(" ".join(digraphs))

ciphertext = playfair_encrypt(digraphs, matrix)

print("\nCiphertext:")
print(ciphertext)

decrypted = playfair_decrypt(ciphertext, matrix)

print("\nDecrypted Text:")
print(decrypted)

frequency = digraph_frequency(ciphertext)

print("\nDigraph Frequency:")
for digraph, count in frequency.items():
    print(digraph, ":", count)

result = verify(plaintext, decrypted, matrix)

print("\nVerification:")
print(result)

print("\nResult:")
print("Playfair Cipher encryption, decryption, frequency analysis, "
      "and verification are successfully implemented.")