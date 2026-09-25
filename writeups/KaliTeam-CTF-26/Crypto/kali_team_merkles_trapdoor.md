# Merkle's Trapdoor — Kali Team CTF 26 (Crypto, 100)

## Challenge
- 100 PTS, 385 solves. Author F4R3S. "Behind every great knapsack lies a hidden trapdoor. Can you find your way through the super-increasing shadows?"
- Given: ciphertext hex `1b99090e0a6109e30414099a090e0a6f211704f4060a20341b99058c060a1c2809d51cbd0a6104e60a6f1cbd21921c281b9921921cbd090320421cbd203f1b990a72` and public key `{14, 5937, 140, 213, 3, 1403, 901, 2009}`.

## Solution
Merkle-Hellman knapsack. 8-element public key → each block of 4 hex digits is one byte (subset sum). Precompute all 2^8 subset sums, map sum→mask, decode each block with bit i = pubkey element i.

```python
blocks = [int(ct[i:i+4], 16) for i in range(0, len(ct), 4)]
mask_to_sum = {}
for mask in range(1 << len(pubkey)):
    mask_to_sum[sum(a for i, a in enumerate(pubkey) if mask & (1 << i))] = mask
print("".join(chr(mask_to_sum[b]) for b in blocks))
```

## Flag
`KaliTeam{M4rK14_h3lLm3n_Kn3ps3cK}`

## Lessons
- Small public key ⇒ exhaustive subset-sum, no trapdoor recovery needed.
- Block count = flag length; block size = encoding unit.
- Technique: research/crypto/merkle_hellman_small_public_key.md
