# ZeroSecure CTF - Crypto Mirror Walk (ROT3 + Atbash)

## Challenge
- **CTF**: ZeroSecure
- **Category**: Crypto
- **Challenge**: Crypto Mirror Walk
- **Files**: `cipher.txt`, `note.txt`

## Given
- Ciphertext: `XsfiEsucfs_UDR{koffif_wjt_epord}`
- Hint: "Three steps forward. Then stand in front of the mirror. What comes back is the message."

## Solution
The hint reveals a two-step decryption:

1. **"Three steps forward"** = Caesar cipher shift +3 (ROT3)
2. **"Stand in front of the mirror"** = Atbash (reverse alphabet: A↔Z, B↔Y, etc.)

Apply in sequence:
- ROT3(XsfiEsucfs_UDR{koffif_wjt_epord}) = AvilHvxfiv_XGU{nriili_zmw_hsrug}
- Atbash(AvilHvxfiv_XGU{nriili_zmw_hsrug}) = ZeroSecure_CTF{mirror_and_shift}

```python
def rot3(text):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr(base + (ord(c) - base + 3) % 26)
        else:
            result += c
    return result

def atbash(text):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr(base + (25 - (ord(c) - base)))
        else:
            result += c
    return result
```

## Flag
`ZeroSecure_CTF{mirror_and_shift}`

## Technique
Compound cipher: Caesar cipher (shift 3) followed by Atbash (reverse alphabet mirror). The challenge name "Mirror Walk" hints at both operations.
