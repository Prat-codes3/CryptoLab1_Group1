from collections import Counter


# 1. Generate 5x5 Playfair key matrix
def generate_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    # Remove duplicate letters from keyword
    key = ""
    for ch in keyword:
        if ch in alphabet and ch not in key:
            key += ch

    # Add remaining alphabet letters
    for ch in alphabet:
        if ch not in key:
            key += ch

    # Create 5x5 matrix
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(list(key[i:i + 5]))

    return matrix


# 2. Prepare plaintext
def prepare_plaintext(plaintext):
    plaintext = plaintext.upper().replace("J", "I")

    # Keep only alphabets
    plaintext = ''.join(ch for ch in plaintext if ch.isalpha())

    return plaintext


# 3. Create digraphs
def create_digraphs(plaintext):
    digraphs = []
    i = 0

    while i < len(plaintext):
        first = plaintext[i]

        # If last character, add X
        if i + 1 >= len(plaintext):
            second = 'X'
            i += 1

        else:
            second = plaintext[i + 1]

            # Repeated letters in a pair
            if first == second:
                second = 'X'
                i += 1
            else:
                i += 2

        digraphs.append(first + second)

    return digraphs


# Find position of a character in matrix
def find_position(matrix, ch):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col


# 4. Playfair encryption
def playfair_encrypt(digraphs, matrix):
    ciphertext = ""

    for pair in digraphs:
        a, b = pair[0], pair[1]

        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        # Same row
        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5]
            ciphertext += matrix[r2][(c2 + 1) % 5]

        # Same column
        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1]
            ciphertext += matrix[(r2 + 1) % 5][c2]

        # Rectangle rule
        else:
            ciphertext += matrix[r1][c2]
            ciphertext += matrix[r2][c1]

    return ciphertext


# 5. Playfair decryption
def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i + 1]

        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        # Same row
        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5]
            plaintext += matrix[r2][(c2 - 1) % 5]

        # Same column
        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1]
            plaintext += matrix[(r2 - 1) % 5][c2]

        # Rectangle rule
        else:
            plaintext += matrix[r1][c2]
            plaintext += matrix[r2][c1]

    return plaintext


# 6. Digraph frequency analysis
def digraph_frequency(ciphertext):
    frequencies = Counter()

    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i + 2]
        frequencies[digraph] += 1

    return frequencies


# 7. Verification
def verify(original_plaintext, decrypted_plaintext, matrix):
    # Prepare original plaintext in the same way
    prepared = prepare_plaintext(original_plaintext)

    # Create the expected Playfair plaintext
    expected_digraphs = create_digraphs(prepared)
    expected = ''.join(expected_digraphs)

    if expected == decrypted_plaintext:
        return "SUCCESS"
    else:
        return "FAILED"


# Main program
keyword = "MONARCHY"
plaintext = "INSTRUMENTS"

# Generate matrix
matrix = generate_key_matrix(keyword)

print("Key Matrix")
for row in matrix:
    print(" ".join(row))

# Prepare plaintext
prepared = prepare_plaintext(plaintext)

# Create digraphs
digraphs = create_digraphs(prepared)

print("\nPrepared Digraphs:")
print(" ".join(digraphs))

# Encrypt
ciphertext = playfair_encrypt(digraphs, matrix)

print("\nCiphertext:")
print(ciphertext)

# Decrypt
decrypted = playfair_decrypt(ciphertext, matrix)

print("\nDecrypted Text:")
print(decrypted)

# Frequency analysis
frequency = digraph_frequency(ciphertext)

print("\nDigraph Frequency:")
for digraph, count in frequency.items():
    print(digraph, ":", count)

# Verification
result = verify(plaintext, decrypted, matrix)

print("\nVerification:")
print(result)

print("\nResult:")
print("Playfair Cipher encryption, decryption, frequency analysis, "
      "and verification are successfully implemented.")