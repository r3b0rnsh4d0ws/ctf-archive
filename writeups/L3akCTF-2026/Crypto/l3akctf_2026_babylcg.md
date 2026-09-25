# L3akCTF 2026 — BabyLCG Writeup

**CTF:** L3akCTF 2026 | **Category:** Crypto | **Difficulty:** Beginner
**Flag:** `L3AK{n3v3r_trU5t_b4s1c_LCG5_frfr}`
**Technique:** LCG recovery from 3 consecutive outputs via modular inverse

## Summary
Classic LCG break: given three outputs (s0, s1, s2) and modulus m, recover multiplier a and increment c, then predict the encryption key (s3). XOR decryption yields the flag.

## Key Math
```
a = (s2 - s1) · (s1 - s0)^{-1} mod m
c = (s1 - a·s0) mod m
key = a·s2 + c mod m
flag = ct XOR key
```

## Gotcha
The modulus m in `chall.py` (placeholder) differed from `output.txt` (actual). Always use the printed value.
