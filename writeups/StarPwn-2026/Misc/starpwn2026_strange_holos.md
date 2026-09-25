# STARPWN 2026 — Strange Holos 1-5 (Misc)

**CTF:** STARPWN 2026 · **Category:** Misc · **Flags:** `STARPWN{...}` × 5

## Challenge
Five AI-generated "glitter" PNG images (`spaceN-glitter.png`, 2.3–2.9 MB each).
Each image carries a custom `caBX` PNG chunk and shows glitter text.
The flag in each image is hidden inside the glitter text — tesseract cannot
read it, a human (or a good OCR engine) can.

## Solve Summary

| # | id | File | Visible text | Cipher | Flag |
|---|----|------|--------------|--------|------|
| 1 | 8  | space1-glitter.png | `GLITTERCITY` | — | `STARPWN{glittercity}` |
| 2 | 9  | space2-glitter.png | `GLITTERCITY` / `FORTUNE` | — | `STARPWN{fortune}` |
| 3 | 10 | space3-glitter.png | `Objgvrf ner pbby!` | ROT13 | `STARPWN{bowties_are_cool}` |
| 4 | 12 | space4-glitter.png | `PAXZOCYY OHVP PCLUTOV TSHT` | unknown | `STARPWN{paxzocyy_ohvp_pclutov_tsht}` |
| 5 | 13 | space5-glitter.png | `IE BEDW QDT JXQDAI VEH QBB JXU FXYIX` | Caesar −10 | `STARPWN{so_long_and_thanks_for_all_the_phish}` |

## Step 1 — the caBX chunk is a red herring
Each PNG is: `IHDR | caBX(29,087 or 24,910 B) | IDAT | IEND`.
The `caBX` chunk is a C2PA content-credential blob (normally chunk type `jumb`,
renamed by the author). Recursive JUMBF parse yields standard boxes:

- `bfdb` (15 B) = `image/svg+xml` content-type
- `bidb` (2415 B) = OpenAI icon SVG (identical in all 5)
- `cbor` actions: `c2pa.created/converted/watermarked.unbound` (gpt-image 2.0)
- `cbor` ocspVals (DER certs; SSL.com C2PA CA for 1–3, Trufo for 4–5)
- `cbor` exclusions + `cbor` claim (instanceID, dc:title `image.png`)
- `cbor` signature = genuine COSE_Sign1 (PS256 for 1–3, ES256 for 4–5)

No trailing bytes, no custom fields, signatures verify structurally →
**the flag is NOT in the metadata** (prior agent's caBX/CBOR theory disproved).

## Step 2 — read the glitter text
The visible content is the flag. Tools that failed: tesseract (all
thresholds/psm), manual ASCII rendering (swirly decorative font).

**Working tool: RapidOCR (ONNX)** — no torch needed:
```
pip install rapidocr_onnxruntime
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()          # 2–4x LANCZOS upscale + autocontrast first
```
Consistent high-confidence reads (0.9–1.0) for every text element.

## Step 3 — decode
- Holos 3: ROT13 of "Bowties are cool!" (Doctor Who, 11th Doctor)
- Holos 5: Caesar shift, plaintext = ciphertext + 10:
  `SO LONG AND THANKS FOR ALL THE PHISH` (Hitchhiker's Guide homage;
  bottom deco: `TOWEL DAY`, `ALWAYS KNOW WHERE YOUR TOWEL IS`).
  Last word `FXYIX` → `PHISH` (visible letters at 0.99 conf; "phish" pun).
- Holos 4: ciphertext `PAXZOCYY OHVP PCLUTOV TSHT` (23 letters, 8-4-7-4).
  Brute-forced Caesar 0–25, ROT13, Atbash, Vigenere (60+ keys incl.
  glittercity/fortune/starpwn/orbit/zodiac), Beaufort, rail fence 2–10,
  columnar transpositions, keyed alphabets, substitution hill-climb — none
  produced English. Flag taken as the readable text in the image.
  (If rejected: the intended plaintext likely a fandom quote; see progress.md)

## Tools / Files
- `solve_holos.py` — caBX extraction + cipher self-check (in each
  `D:\CTF\ctfs\0_starpwn2026\misc\1_Strange_Holos_N\` folder with progress.md)
- RapidOCR (rapidocr_onnxruntime) — the key OCR engine
- Per-challenge progress: `D:\CTF\ctfs\0_starpwn2026\misc\1_Strange_Holos_{1..5}\progress.md`
- Series progress: `D:\CTF\ctfs\0_starpwn2026\misc\progress_holos.md`
