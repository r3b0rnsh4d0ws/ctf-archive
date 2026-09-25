# Score Quest — Reverse Engineering Challenge

## Goal
You are given a small game binary (`scorequest`). The game awards points for correct
guesses, but the score needed to "win" is set so high that reaching it by actually
playing is effectively impossible. When the score gate is passed, the program prints
the **flag**.

Your job: obtain the flag **without cheating by reading it out of the binary's
strings or memory**.

## Rules (what you are NOT allowed to do)
- The flag is **encrypted** at rest — it is never stored in plaintext, so `strings`,
  `grep`, or a memory dump taken during normal play will not show it.
- If you attach a debugger (`gdb`, `x64dbg`, `windbg`, ...) the decryption is
  deliberately corrupted, so breaking at the reveal and reading memory only yields
  garbage.

## Intended path (what you SHOULD do)
Reverse engineer the binary, find the score-gate / scoring logic, and **trigger the
reveal mechanism**. The simplest legitimate approach is to analyze how the score is
checked and modify that check (or the score itself) so the gate fires, then run the
binary **normally** (no debugger) to let it decrypt and print the flag.

The flag is only ever reconstructed in RAM for the moment it is printed, so you must
make the program reach the reveal code on its own.

## Building
```
# Linux / WSL
make                 # builds ./scorequest and runs gen_flag.py

# Custom flag:
FLAG="CTF{your_flag_here}" python3 gen_flag.py && make

# Windows (MinGW)
gcc -O2 -o scorequest.exe challenge.c
```
Requires Python 3 to generate `flag_data.h` (the encrypted flag container).

## Files
- `challenge.c`  — the game + encrypted-flag reveal logic
- `gen_flag.py`  — encrypts the flag into `flag_data.h`
- `flag_data.h`  — auto-generated encrypted flag (regenerate to change the flag)
- `Makefile`     — build helper
