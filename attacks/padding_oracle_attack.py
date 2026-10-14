from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16


class PaddingOracleDemo:

    def __init__(self, key, iv, ciphertext):
        self.__key = key
        self.iv = iv
        self.ciphertext = ciphertext
        self.queries = 0

    def valid_padding(self, ciphertext, iv=None):
        self.queries += 1
        if iv is None:
            iv = self.iv
        try:
            raw = AES.new(self.__key, AES.MODE_CBC, iv).decrypt(ciphertext)
            unpad(raw, BLOCK_SIZE, style="pkcs7")
            return True
        except ValueError:
            return False


def recover_block(oracle, previous_block, target_block):

    intermediate = bytearray(BLOCK_SIZE)
    recovered = bytearray(BLOCK_SIZE)
    crafted = bytearray(previous_block)

    for pad_value in range(1, BLOCK_SIZE + 1):
        index = BLOCK_SIZE - pad_value

        for j in range(index + 1, BLOCK_SIZE):
            crafted[j] = intermediate[j] ^ pad_value

        found = False
        for guess in range(256):
            crafted[index] = guess
            if not oracle.valid_padding(bytes(target_block), iv=bytes(crafted)):
                continue

            if pad_value == 1 and index > 0:
                probe = bytearray(crafted)
                probe[index - 1] ^= 1
                if not oracle.valid_padding(bytes(target_block), iv=bytes(probe)):
                    continue

            intermediate[index] = guess ^ pad_value
            recovered[index] = intermediate[index] ^ previous_block[index]
            found = True
            break

        if not found:
            raise RuntimeError(
                f"Could not recover byte at position {index}. "
                "Check the oracle interface and ciphertext format."
            )

    return bytes(recovered)


def padding_oracle_attack(oracle, iv, ciphertext):
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be exactly 16 bytes.")
    if not ciphertext or len(ciphertext) % BLOCK_SIZE:
        raise ValueError("Ciphertext must contain complete AES blocks.")

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    plaintext = bytearray()
    previous = iv
    for target in blocks:
        plaintext.extend(recover_block(oracle, previous, target))
        previous = target

    padding_length = plaintext[-1]
    if not 1 <= padding_length <= BLOCK_SIZE:
        raise RuntimeError("Recovered plaintext has invalid padding.")
    if plaintext[-padding_length:] != bytes([padding_length]) * padding_length:
        raise RuntimeError("Recovered plaintext has invalid PKCS#7 padding.")

    return bytes(plaintext[:-padding_length])


def main():

    key = get_random_bytes(BLOCK_SIZE)
    iv = get_random_bytes(BLOCK_SIZE)
    message = b"This is test plaintest"
    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(message, BLOCK_SIZE))

    oracle = PaddingOracleDemo(key, iv, ciphertext)
    queries_before = oracle.queries
    recovered = padding_oracle_attack(oracle, iv, ciphertext)
    query_count = oracle.queries - queries_before

    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Recovered plaintext:", recovered.decode("utf-8"))
    print("Oracle queries:", query_count)


if __name__ == "__main__":
    main()
