import os
import math
import shutil
import subprocess
from collections import Counter

# Generate 1 MiB of random data
SIZE = 1024 * 1024


# --------------------------------------------------
# 1. GENERATE RANDOM DATA USING /dev/urandom
# --------------------------------------------------

def generate_urandom():
    with open("/dev/urandom", "rb") as source:
        data = source.read(SIZE)

    with open("linux_random.bin", "wb") as file:
        file.write(data)

    print("[+] Generated linux_random.bin using /dev/urandom")


# --------------------------------------------------
# 2. GENERATE RANDOM DATA USING OPENSSL
# --------------------------------------------------

def generate_openssl():
    if shutil.which("openssl") is None:
        print("[!] OpenSSL is not installed.")
        print("    Install it using: sudo apt install openssl")
        return False

    try:
        with open("openssl_random.bin", "wb") as file:
            subprocess.run(
                ["openssl", "rand", str(SIZE)],
                stdout=file,
                check=True
            )

        print("[+] Generated openssl_random.bin using OpenSSL")
        return True

    except subprocess.CalledProcessError:
        print("[!] OpenSSL generation failed.")
        return False


# --------------------------------------------------
# 3. CHI-SQUARE P-VALUE
# Uses SciPy if available
# --------------------------------------------------

def chi_square_p_value(statistic, degrees_of_freedom):
    try:
        from scipy.stats import chi2
        return chi2.sf(statistic, degrees_of_freedom)
    except ImportError:
        return None


# --------------------------------------------------
# 4. ANALYZE RANDOM DATA
# --------------------------------------------------

def analyze_file(filename):
    if not os.path.exists(filename):
        print("\n[!] File not found:", filename)
        return

    with open(filename, "rb") as file:
        data = file.read()

    n = len(data)

    if n == 0:
        print("\n[!] Empty file:", filename)
        return

    print("\n" + "=" * 60)
    print("FILE:", filename)
    print("=" * 60)

    print("File size:", n, "bytes")

    # ----------------------------------------------
    # A. BYTE FREQUENCY DISTRIBUTION
    # ----------------------------------------------

    frequencies = [0] * 256

    for byte in data:
        frequencies[byte] += 1

    expected = n / 256

    chi_square = sum(
        (observed - expected) ** 2 / expected
        for observed in frequencies
    )

    p_value = chi_square_p_value(chi_square, 255)

    print("\nA. BYTE FREQUENCY DISTRIBUTION")
    print("Expected frequency per byte:", expected)
    print("Minimum frequency:", min(frequencies))
    print("Maximum frequency:", max(frequencies))
    print("Chi-square statistic:", round(chi_square, 4))

    if p_value is not None:
        print("Chi-square p-value:", p_value)

        if p_value < 0.01:
            print("Result: Significant deviation detected.")
        else:
            print("Result: No significant deviation detected.")
    else:
        print("P-value unavailable: install SciPy for this test.")
        print("Command: python3 -m pip install scipy")

    # ----------------------------------------------
    # B. BIT DISTRIBUTION / MONOBIT TEST
    # ----------------------------------------------

    ones = sum(byte.bit_count() for byte in data)
    total_bits = n * 8
    zeros = total_bits - ones

    z_score = (ones - total_bits / 2) / math.sqrt(total_bits / 4)

    # Two-sided normal approximation
    monobit_p = math.erfc(abs(z_score) / math.sqrt(2))

    print("\nB. BIT DISTRIBUTION")
    print("Total bits:", total_bits)
    print("Number of zero bits:", zeros)
    print("Number of one bits:", ones)
    print("Percentage of ones:", round(ones / total_bits * 100, 4))
    print("Monobit z-score:", round(z_score, 4))
    print("Monobit p-value:", monobit_p)

    if monobit_p < 0.01:
        print("Result: Significant bit imbalance detected.")
    else:
        print("Result: No significant bit imbalance detected.")

    # ----------------------------------------------
    # C. REPEATED ADJACENT BYTES
    # ----------------------------------------------

    adjacent_repeats = sum(
        data[i] == data[i - 1]
        for i in range(1, n)
    )

    print("\nC. REPEATED PATTERNS")
    print("Adjacent equal-byte pairs:", adjacent_repeats)

    # ----------------------------------------------
    # D. REPEATED NON-OVERLAPPING 16-BYTE BLOCKS
    # ----------------------------------------------

    block_size = 16

    blocks = [
        data[i:i + block_size]
        for i in range(0, n - block_size + 1, block_size)
    ]

    block_counts = Counter(blocks)

    repeated_blocks = sum(
        count - 1
        for count in block_counts.values()
        if count > 1
    )

    print("Repeated 16-byte blocks:", repeated_blocks)

    # ----------------------------------------------
    # E. SERIAL CORRELATION
    # ----------------------------------------------

    mean = sum(data) / n

    numerator = sum(
        (data[i] - mean) * (data[i + 1] - mean)
        for i in range(n - 1)
    )

    denominator = sum(
        (byte - mean) ** 2 for byte in data
    )

    correlation = numerator / denominator if denominator else 0

    print("\nD. SERIAL CORRELATION")
    print("Adjacent-byte correlation:", round(correlation, 6))

    if abs(correlation) < 0.01:
        print("Result: Low observed linear correlation.")
    else:
        print("Result: Non-negligible observed correlation; investigate.")

    # ----------------------------------------------
    # F. FINAL SUMMARY
    # ----------------------------------------------

    print("\nE. SUMMARY")
    print("Data analyzed:", filename)
    print("Byte-frequency statistic:", round(chi_square, 4))
    print("Bit-balance p-value:", monobit_p)
    print("Serial correlation:", round(correlation, 6))
    print("Note: Statistical tests cannot prove cryptographic security.")


# --------------------------------------------------
# 5. MAIN PROGRAM
# --------------------------------------------------

def main():
    print("RANDOM NUMBER GENERATOR ANALYSIS")
    print("-" * 40)

    generate_urandom()
    generate_openssl()

    print("\nStarting statistical analysis...")

    analyze_file("linux_random.bin")
    analyze_file("openssl_random.bin")

    print("\n[+] Analysis completed.")


if __name__ == "__main__":
    main()