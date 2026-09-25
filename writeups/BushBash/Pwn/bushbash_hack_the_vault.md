# BushBash - Hack The Vault I (Pwn, Beginner)

## Flag
`bushbash{th1s-is-just-th3-beginning!}`

## Challenge
Jungle/Moss Man/detective Kane storyline. `nc 34.40.133.67 7776`. Binary: `vault` (ELF64 PIE, stripped). Author: Harold Gao.

## Solution
- `strings -n 4 vault` → hardcoded password in .rodata: `th3M0ssM4ni5h3re,y0uc4ntcatchm3`
- Check logic: `fgets(buf,0x100)` → strip `\n` → length must equal `strlen(pw)` → `strncmp(input, pw, n)`
- Send the full password (comma included) → `bushbash{th1s-is-just-th3-beginning!}`

## Authoring Notes
- Literal `.rodata` password + `fgets`/`strncmp` gate; stripped+PIE+canary as hardening theater (irrelevant for string compare)
- Leetspeak (`th3M0ssM4ni5h3re...`) gives a minor decode step
- Storyline teases sequel — success message: "this case is not over just yet... stop the Moss Man at all costs"

## Lessons
- `strings` before deep analysis — hardcoded creds are the #1 beginner pattern
- Exact-match comparisons (length check + strncmp): copy every byte including punctuation
- `fopen`+`fread`+`strncmp` imports = "enter password → print flag.txt"
