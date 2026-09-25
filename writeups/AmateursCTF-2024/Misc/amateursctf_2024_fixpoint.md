# AmateursCTF 2024 — fixpoint (misc)

**Files:** `fixpoint.py`, `readme.md`
**Flag:** `bctf{DEPCmQqklUgj5yNBA93IHMYaVFiXedxroKsh4GuSvJW72OzwLR6Z8p01nT}`
**Artifacts kept:** `solve_fixpoint.py`, `verify_fixpoint.py`, this writeup

## Summary
Repeated base64 encoding of any string converges to a fixed point (standard alphabet: the
famous `Vm0wd2Qy...` string). This challenge uses a **custom base64 alphabet**
`bctf{?????????????????????????FiXed???????????????????????p01nT}` (64 chars, 16 known,
48 unknown) and gives the resulting fixed point prefix `NslSBwm6YNH...`. The 48 unknown
alphabet characters ARE the flag (`bctf{...}`).

## Key insight
For the infinite fixed point `P`, `P = encode(P)`, so `decode(P)` is a prefix of `P`.
Therefore for every window: `encode(P[3k:3k+3]) = P[4k:4k+4]`. The 3 input bytes are the
ASCII codes of `P[3k..3k+2]`; the 4 output chars must be `P[4k..4k+3]`. With custom alphabet
index mapping this yields, per window:
```
alphabet[b0>>2] = P[4k]
alphabet[((b0&3)<<4)|(b1>>4)] = P[4k+1]
alphabet[((b1&0xF)<<2)|(b2>>6)] = P[4k+2]
alphabet[b2&0x3F] = P[4k+3]
```
Each window pins 4 alphabet positions. Collecting constraints over the whole 1000-char fixed
point pins **all 64 positions with zero conflicts** → alphabet recovered.

## Solution
1. Extract the custom fixed point `F` (second `fixed_point = "..."` in the file).
2. For `k` in `0..len(F)//4`: compute the 4 indices from `ord(F[3k]),ord(F[3k+1]),ord(F[3k+2])`
   and pin `alphabet[idx] = F[4k+t]`.
3. Merge with the 16 known positions (`bctf{FiXedp01nT}`) — no conflicts, nothing unfilled.
4. Verify: `encode(F)` starts with `F`; `F` is a fixed point after one iteration;
   `decode(F)` is a prefix of `F`; arbitrary strings converge to `F` (≈27 iterations);
   patched `fixpoint.py` prints `Found the fixed point, and it is what I expected!`.

## Gotchas
- `base64.b64encode(...).decode().replace('=','')` — the fixed point has no padding; the
  window alignment is exact (no `=`), so `4k` output windows line up perfectly.
- The alphabet is a bijection (64 distinct chars) — consistency of the constraints confirms it.
- The flag IS the full 64-char alphabet string (already in `bctf{...}` format), including the
  decoy-looking `FiXed` and `p01nT` substrings.

## Verification
- Alphabet: `bctf{DEPCmQqklUgj5yNBA93IHMYaVFiXedxroKsh4GuSvJW72OzwLR6Z8p01nT}`
- `encode(F)` prefix ✓, fixed point after 1 iter ✓, arbitrary string converges to F ✓,
  patched script prints the expected message ✓.
