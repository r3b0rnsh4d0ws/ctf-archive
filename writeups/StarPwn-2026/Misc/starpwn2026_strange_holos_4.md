# STARPWN 2026 — Strange Holos 4 (Misc, id 12)

**CTF:** STARPWN 2026 · **Category:** Misc (steg/OCR + Vigenere) · **Flag:** `STARPWN{i_am_sorry_dave_i_cant_do_that}`

## Challenge
`space4-glitter.png` (2.65 MB) — AI-generated glitter image (gpt-image 2.0) showing
swirly decorative text. Prior agent OCR'd it but could NOT crack the cipher and
wrongly recorded the raw ciphertext as the flag (that flag was never even submitted
to the platform — CTFd `attempts: 0`, `solved_by_me: false`).

## Step 1 — OCR the glitter text
- tesseract: FAILS on glitter (noise).
- RapidOCR (`rapidocr_onnxruntime`): reads consistently at 0.93–0.99 conf:
  ```
  PAXZOCYY OHVP, PCLUTOV TSHT
  ```
  4 words, lengths 8-4-7-4, comma after OHVP (punctuation deco). Verified with
  3x upscale, per-region crops, and tile scans. No GLITTERCITY brand watermark in
  this image (unlike siblings 1-3).

## Step 2 — identify the cipher
Sibling holos used simple monoalphabetic ciphers:
- Holos 3: ROT13 ("Objgvrf ner pbby!" → "BOWTIES ARE COOL")
- Holos 5: Caesar +10 ("IE BEDW QDT JXQDAI..." → "SO LONG AND THANKS FOR ALL THE PHISH")

For Holos 4, `PAXZOCYY OHVP PCLUTOV TSHT` has cross-word letter reuse
(P in w1/w2/w3, O in w1/w2/w3, T in w3/w4, H in w2/w4, V in w2/w3) which looks
monoalphabetic, but:
- Caesar 0-25 / ROT13 / Atbash / Affine → no English
- Monoalphabetic substitution solver (word-pattern + cross-word constraint,
  wordfreq + words_alpha + fandom proper nouns) → **0 valid solutions**
- Keyword substitution alphabets (GLITTERCITY, PRISMANTIR, HOLO, ...) → no
- Rail fence, columnar, Playfair, Bifid, Foursquare, ADFGX, Gronsfeld, Porta,
  Autokey, Beaufort with theme keys → no

**Key pivot: Vigenere/Beaufort dictionary-key attack with n-gram scoring.**
Brute-forcing ~57k English words as Vigenere keys with a trigram English model
instantly surfaces (score −184.8 vs −213 next best):

```
key = HAL  →  I AM SORRY DAVE I CANT DO THAT
```

The HAL 9000 catchphrase from *2001: A Space Odyssey* — perfect space theme.
Split by ciphertext word lengths: `IAMSORRY DAVE ICANTDO THAT` (8-4-7-4 ✓).

## Step 3 — verify
Vigenere encrypt of `IAMSORRY DAVE ICANTDO THAT` with key `HAL` reproduces
`PAXZOCYY OHVP PCLUTOV TSHT` **exactly** (round-trip verified).

## Flag
```
STARPWN{i_am_sorry_dave_i_cant_do_that}
```

## Tools / Files
- RapidOCR (ONNX) — OCR the glitter text
- wordfreq + words_alpha — dictionaries
- python Vigenere with n-gram scoring — key recovery (key=HAL)
- Kept: solve scripts in `D:\CTF\ctfs\0_starpwn2026\misc\1_Strange_Holos_4\`
- Original challenge file: `D:\CTF\ctfs\0_starpwn2026\misc\all_holos\space4-glitter.png`
