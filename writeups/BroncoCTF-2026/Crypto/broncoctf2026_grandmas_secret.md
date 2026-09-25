# BroncoCTF 2026 - Grandma's Secret

**Category:** Cryptography
**Score:** 100
**Status:** Solved
**Flag:** `bronco{JELLYDONUT}`

## Challenge Description

> Grandma left you a secret message in her recipe book. Can you figure out what it says?
>
> Ciphertext: `GVXX FVXV AFXF XVGA DAFF`
>
> Key: SUGAR
>
> Grid from Letter.jpeg (6x6 ADFGVX grid)

## Analysis

### Cipher Identification

The ciphertext consists of pairs of letters from the set {A, D, F, G, V, X}, which immediately identifies this as an **ADFGVX cipher** - a fractionating transposition cipher used by the German Army in WWI.

### Grid Reconstruction

From the provided Letter.jpeg image, we reconstruct the 6x6 Polybius square:

```
     A  D  F  G  V  X
  A | B  3  M  R  L  I
  D | A  6  F  O  8  2
  F | C  7  S  E  U  H
  G | Z  9  D  X  K  V
  V | 1  Q  Y  W  5  P
  X | N  J  T  4  G  O
```

### Decryption Process

1. **Substitution (ADFGVX → Plaintext pairs):**
   Each ciphertext letter pair maps to a grid coordinate, which gives us the intermediate text after undoing the substitution.

   Ciphertext: `GVXX FVXV AFXF XVGA DAFF`
   Pairs: `GV XX FV XV AF XF XV GA DA FF`

   Using the grid:
   - GV → row G, col V → K
   - XX → row X, col X → O
   - FV → row F, col V → U
   - XV → row X, col V → G
   - AF → row A, col F → R
   - XF → row X, col F → J
   - XV → row X, col V → G
   - GA → row G, col A → Z
   - DA → row D, col A → A
   - FF → row F, col F → S

   Intermediate: `KOU GRJG ZAS`

   Wait, that doesn't look right. Let me re-examine.

   Actually, the ADFGVX cipher first does a **substitution** (using the grid) then a **columnar transposition** with the key. To decrypt, we reverse the process:

   1. First undo the columnar transposition
   2. Then undo the substitution

3. **Columnar Transposition Decryption:**
   
   Key: SUGAR
   Key length: 5
   Alphabetical order of key: A(0), G(1), R(2), S(3), U(4)
   
   Original key positions: S(0), U(1), G(2), A(3), R(4)
   Sorted by letter: A(3), G(2), R(4), S(0), U(1)
   Column order: 3, 2, 4, 0, 1

   Ciphertext: `GVXXFVXVAFXFXVGADAFF` (20 chars)
   Rows = 20/5 = 4

   Fill columns in alphabetical key order (3, 2, 4, 0, 1):
   
   Column 3 (A): GVXX
   Column 2 (G): FVXV
   Column 4 (R): AFXF
   Column 0 (S): XVGA
   Column 1 (U): DAFF

   Grid (4 rows × 5 cols):
   ```
   G F A X D
   V V F V A
   X X X G F
   X V F A F
   ```

   Read row-wise: `GFAXD VVXFA XXXGV XVFAF`

   That's 20 chars. Now substitute using the grid.

   Actually, let me use the solver script which correctly handles this.

## Solution

Running the provided solver script yields:

```
After undoing transposition: XDFGAVAVVFGFXXXAFVXF
Flag: JELLYDONUT
BroncoCTF flag: bronco{JELLYDONUT}
```

The decrypted plaintext is `JELLYDONUT`, giving the flag `bronco{JELLYDONUT}`.

## Solution Code

The provided `solve.py` correctly implements the ADFGVX decryption:

```python
#!/usr/bin/env python3
"""
Grandma's Secret - ADFGVX Cipher Solver
Ciphertext: GVXX FVXV AFXF XVGA DAFF
Key: SUGAR
Grid from image:
     A  D  F  G  V  X
  A | B  3  M  R  L  I
  D | A  6  F  O  8  2
  F | C  7  S  E  U  H
  G | Z  9  D  X  K  V
  V | 1  Q  Y  W  5  P
  X | N  J  T  4  G  O
"""

ciphertext = "GVXXFVXVAFXFXVGADAFF"
key = "SUGAR"

# ... ADFGVX decryption implementation ...
```

## Lessons Learned

1. **ADFGVX is a two-step cipher:** First a Polybius square substitution, then columnar transposition
2. **Order matters:** Must undo transposition FIRST, then substitution
3. **Key scheduling:** Columnar transposition key order is determined by alphabetical sorting of the key letters
4. **Grid reconstruction:** Critical to accurately extract the 6x6 grid from the image

## Tools Used

- Custom Python solver (`solve.py`, `solve2.py`, `solve3.py`)
- Manual verification of grid coordinates

## References

- [ADFGVX Cipher - Wikipedia](https://en.wikipedia.org/wiki/ADFGVX_cipher)
- [CTF Crypto - ADFGVX](https://cryptohack.org/courses/intro/adfgvx/)