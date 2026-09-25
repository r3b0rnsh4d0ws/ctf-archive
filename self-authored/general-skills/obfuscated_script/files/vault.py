#!/usr/bin/env python3
# "Advanced polymorphic anti-tamper flag vault (TM)." Paid reviewers loved it.
import base64, hashlib, zlib, os

# --- decoy: this whole block does nothing useful -------------------------
__VAULT__ = b"eJzLVspIzcnJ11EoLcrMS1coSy0uCUotLS/PyU9RSs1Lz8tMTgUAZPcHQQ=="
__KEY__   = hashlib.sha256(b"totally-secret-key").digest()
__NONCE__ = bytes([(i * 7 + 3) % 256 for i in range(16)])

def _decrypt(blob):
    raw = zlib.decompress(base64.b64decode(blob))
    return bytes([raw[i] ^ __KEY__[i % len(__KEY__)] ^ __NONCE__[i % 16] for i in range(len(raw))])

def __obfuscated_core__():
    exec(base64.b64decode(b"cHJpbnQoJ2NhbGN1bGF0aW5nIHNlY3JldCB2YXVsdC4uLicp").decode())

# --- the real answer is reconstructed below, not stored as a string -------
_FLAG_CODES__ = [102, 108, 97, 103, 123, 111, 98, 102, 117, 115, 99, 97, 116, 105, 111, 110, 95, 105, 115, 95, 106, 117, 115, 116, 95, 115, 101, 99, 117, 114, 105, 116, 121, 95, 116, 104, 101, 97, 116, 101, 114, 125]

if __name__ == "__main__":
    __obfuscated_core__()
    print("decrypting vault (this is where it gets slow)...")
    flag = "".join(chr(c) for c in _FLAG_CODES__)
    print(flag)