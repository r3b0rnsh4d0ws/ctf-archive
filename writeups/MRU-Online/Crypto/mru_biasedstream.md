# mruonline - biasedstream (LFSR Stream Cipher)

## Challenge
- **CTF**: mruonline
- **Category**: crypto
- **Challenge**: biasedstream
- **Files**: `cipherstreamer.py`, `output.bin` (28 bytes encrypted)

## Components

- **LFSR**: 8-bit, initial state=0x37, feedback poly=0xB8 (x⁸+x⁵+x⁴+x³+1)
- **Second layer**: XOR with 0xAA after LFSR decoding

## Solution

```python
ct = bytes.fromhex("a606c9deccd1c8c3cbd9cfcef5d9ded8cfcbc7f5c6cfcbc1cbcdcfd7")
state = 0x37
key = []
for _ in range(len(ct)):
    t = state
    u = (t >> 7) & 1
    state = ((t << 1) ^ (0xB8 & (-u))) & 0xFF
    key.append(state)
intermediate = bytes([c ^ k for c, k in zip(ct, key)])
plaintext = bytes([b ^ 0xAA for b in intermediate])
```

## Flag
`bpctf{biased_stream_leakage}`
