
import ctypes
from ctypes import wintypes

bcrypt = ctypes.WinDLL("bcrypt")

BCryptGenRandom = bcrypt.BCryptGenRandom
BCryptGenRandom.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_ubyte),
    wintypes.ULONG,
    wintypes.ULONG
]
BCryptGenRandom.restype = wintypes.LONG

BCRYPT_USE_SYSTEM_PREFERRED_RNG = 0x00000002


def generate_random_bytes(size):
    buffer = (ctypes.c_ubyte * size)()

    status = BCryptGenRandom(
        None,
        buffer,
        size,
        BCRYPT_USE_SYSTEM_PREFERRED_RNG
    )

    if status != 0:
        raise OSError(
            f"BCryptGenRandom failed with NTSTATUS 0x{status & 0xFFFFFFFF:08X}"
        )

    return bytes(buffer)
