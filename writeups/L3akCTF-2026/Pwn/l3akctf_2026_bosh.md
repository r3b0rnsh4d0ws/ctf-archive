# L3akCTF 2026 — Bosh (Pwn, 500 pts)

**Flag:** `L3AK{ever_H3arD_of_4_s36faul7_or4c13}`

| Field | Value |
|-------|-------|
| CTF | L3akCTF 2026 |
| Challenge | Bosh |
| Category | Pwn |
| Points | 500 |
| Difficulty | Medium (intended) / Easy (actual) |
| Solve Method | Direct `cat flag.txt` (chmod bypass) |
| Technique | Segfault oracle / global buffer overflow / fake module_t |
| Source | `D:\CTF\ctfs\0_l3akctf\pwn\1_bosh\writeup.md` |

## Vulnerability Summary

1. **chmod(0) bypass:** Service runs as root; `chmod("flag.txt", 0)` doesn't prevent `cat flag.txt`
2. **Global buffer overflow:** `memcpy(previousCommand, cmdBuf, cmdLen)` overflows into `modules_head`, `pointers[]`, `moduleCounter`
3. **"prev" replay:** TCP preserves NUL bytes → `prev\x00` matches `strcmp` → re-executes corrupted buffer
4. **Fake module_t:** Overflow `modules_head` to point into previousCommand → fake struct with arbitrary `code` pointer → `m->code(pointers, args)` = controlled rdi/rsi
5. **Segfault oracle (intended):** `ray` module = one-shot byte write + crash observation = 1-bit oracle per byte (flag name hints at this)
6. **Fixed mmap:** `0x1337000 + n*0x1000` — no ASLR for module code
