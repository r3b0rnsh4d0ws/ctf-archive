# LIT CTF 2026 — HelloWorld (misc)

## Challenge
- Category: misc (0-pt demo)
- Description: "Here's an easy CTF problem for demonstration purposes. I will go get some caesar salad while you solve this."
- Flag format: `LITCTF{...}`
- File: `helloworld.txt` → `YVGPGS{J3yp0z3_G0_Y1GPGS}`

## Technique
ROT13 Caesar cipher:
- "caesar salad" hint → Caesar; `LITCTF{` → `YVGPGS{` confirms shift **+13** = ROT13
- Letters only, digits/braces pass through
- ROT13 is self-inverse

## Flag
```
LITCTF{W3lc0m3_T0_L1TCTF}
```

## Lessons
1. Known-prefix shift verification: derive the shift from the flag format prefix instead of brute-forcing all 25 shifts.
2. PowerShell `-match` is case-insensitive by default — use `-cmatch` for `[A-Z]`/`[a-z]` classification in ROT implementations (else wrong base → garbled output).
3. Authoring note: demo challenge = single text file with the flag as the sole line, trivial cipher, designed to teach flag format + file download + submission.

## Artifacts
- Challenge folder: `D:\CTF\ctfs\1_litctf\misc\1_helloworld\` (progress.md, writeup.md, helloworld.txt)
