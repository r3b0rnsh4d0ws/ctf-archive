# SCONES blowfish — per-block signature forgery over CBC

- **CTF:** SCONES (chal.secso.cc:2001) | **Category:** crypto | **Difficulty:** hard (100)
- **Flag:** `SCONES{great_work_infiltrating_as_the_head_fish_perhaps_one_could_call_you_james_pond}`
- **Files:** `D:\CTF\ctfs\scones\crypto\blowfish\` (server.py, exploit.py, blowhandout.zip)

## TL;DR
Blowfish-CBC server signs each 8-byte block with `sha256(KEY + block)` — signature depends only on block content. Build a pool of signed blocks (fish plaintext + ciphertext from encrypt rounds). Any block in the odd-fold XOR span of the pool is manufacturable as a signed block via: encrypt `s_a||s_b` → C_b (D(C_b)=s_a^s_b known), decrypt `s_c||C_b||C_d` → signed middle block s_a^s_b^s_c. Gaussian elimination over GF(2)^64 (with index-set tracking) expresses target `: true} ` as an odd-fold XOR; fish block 0 is already `{"admin"`. Submit `iv || '{"admin"' || ': true} '` fully signed → flag.

## Key steps
1. Parse fish + signature → 151 signed blocks; 4 encrypt rounds → 755 blocks (rank 64).
2. Basis of W = span{p_i ^ p1}; express T^p1; parity-adjust to odd-fold representation (33 terms).
3. 16 iterative 3-fold additions (encrypt+decrypt each) → target signed.
4. Final submit → flag.

## Lessons
- Per-block content-only signatures = block reuse forgery.
- CBC decrypt oracle signs D(C_b) XOR C_a — linear structure over GF(2)^64.
- 3-block decrypt keeps target in middle (unpad-safe).
- Gaussian elimination: track index sets (symmetric difference), not single indices.