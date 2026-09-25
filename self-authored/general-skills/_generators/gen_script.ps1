$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\obfuscated_script"
$out  = "$base\files\vault.py"
$flag = "flag{obfuscation_is_just_security_theater}"

# store as char codes so the literal never appears in the source
$codes = [int[]]($flag.ToCharArray() | ForEach-Object { [int]$_ })
$codesLine = "[" + ($codes -join ", ") + "]"

$py = @"
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
_FLAG_CODES__ = $codesLine

if __name__ == "__main__":
    __obfuscated_core__()
    print("decrypting vault (this is where it gets slow)...")
    flag = "".join(chr(c) for c in _FLAG_CODES__)
    print(flag)
"@
Set-Content -Path $out -Value $py -NoNewline
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "codes count: $($codes.Length)"