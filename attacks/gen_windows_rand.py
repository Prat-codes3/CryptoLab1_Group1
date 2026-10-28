
from pathlib import Path
from CNG_random import generate_random_bytes

SIZE = 1024 * 1024
OUTPUT_FILE = Path("windows_random.bin")

data = generate_random_bytes(SIZE)
OUTPUT_FILE.write_bytes(data)

print("Windows CNG random data generated successfully.")
print(f"File: {OUTPUT_FILE.resolve()}")
print(f"Bytes written: {OUTPUT_FILE.stat().st_size}")
