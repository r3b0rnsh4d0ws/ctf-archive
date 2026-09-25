# Kali Team CTF 26 - Fault Cartography (RE, hard)

## Challenge
Stripped ELF64 PIE `faultline` + `faultline.map` (6,222 bytes). The binary walks a 16x16 fault map for 104 steps; each cell deliberately triggers a CPU fault (SIGILL/SIGFPE/SIGSEGV) whose handler mutates a 48-byte route buffer using the cell's decrypted fields. Correct route => mutated buffer equals decrypted header block D => "the map remembers you" (exit 0). Wrong => "lost" (exit 1).

## Files
`D:\CTF\ctfs\1_kali-team-ctf\re\01_fault_cartography\` (faultline, faultline.map, solve_fault.py, fault_gdb.cmd, writeup.md, progress.md)

## Technique (full solve)
1. Static RE of the stripped PIE: main@0x1280, signal handler@0x1ae0, fault trigger@0x1ab0 (ud2 | div-by-zero | write [0]), recovery via sigsetjmp(0x4080,1)/__longjmp_chk.
2. Header: magic FLT2, version 2, 78-byte header + 256x24-byte entries; splitmix64 finalizer hash check (True); start (1,14); 104 steps.
3. splitmix64 finalizer (f64) is the keyed PRF for EVERYTHING, each purpose with its own xor constant:
   - entry decrypt: f64(hdr_q ^ i*0xA0761D6478BD642F ^ idx*0xD6E8FEB86659FD93 ^ 0x6A09E667F3BCC909)
   - state chain: f64(state ^ q2 ^ y ^ (x<<8) ^ step*0x9E3779B97F4A7C15); initial f64(hdr_q ^ 0x1BD11BDAA9FC1A22)
   - route keystream (CFB): f64(hdr_q ^ i*0x9E3779B97F4A7C15 ^ 0xBADC0FFEE0DDF00D)
   - final D: per byte f64((i>>3)*0xE7037ED1A0B428DB ^ state ^ 0x243F6A8885A308D3)
4. Handler ops (route = 6 qwords):
   - ILL b1=0: route[b2%6] += rol64(route[b3%6]^c, b4)
   - ILL b1=1: route[b2%6] = K*(c+route[b2%6]), K = ((v<<48)|(v<<16)|(v^0xA55A))|1
   - FPE b1=0: swap-with-rol (recoverable pair)
   - FPE b1=1: route[b2%6] ^= rol64(route[b3%6]^c, b4&0x3f)
   - SEGV b1=0: right-rotate whole buffer by n=(((b2%6)%5)+1)%6
   - SEGV b1=1: route[b2%6] = rol64(route[b2%6]^c, b4)
5. Inversion: start from R_final = D, apply ops in reverse (mul needs modular inverse of odd K; swap recoverable; no op uses b2==b3 so lanes stay independent), then XOR the CFB keystream to get the plaintext route.

## Verification method (the important part)
Forward model was verified byte-exactly against gdb before trusting the inversion:
- gdb harness: starti -> pending break fopen -> base = *(u64*)$rsp - 0x12c7 (fopen's return address into main); `handle SIGILL SIGFPE SIGSEGV nostop noprint pass` so the binary's own handler runs under gdb; break at loop top 0x18c3 (after globals stored, BEFORE the op) and dump the route buffer every iteration (104 ITER lines).
- First divergence pinpointed the bug: step 2, the first mul op. The K constant had been misread as v|v<<32 instead of v<<48|v<<16 (imul 0x1000000010000). One-line fix; then all 104 ITER dumps AND the final compare dump matched byte-exactly.

## Flag
`KaliTeam{faults_draw_the_only_honest_path}` (verified locally: "the map remembers you", exit 0)

## Authoring notes (how to build this)
- Map = encrypted per-cell command records (24 bytes = 3 qwords); header carries magic/version/steps/route-length/start-nibble-keys + a splitmix64 checksum + the encrypted expected output D. Flag IS the 42-byte plaintext route (KaliTeam{ + 32 + }).
- The fault cartography is the obfuscation: every op is triggered via a real CPU fault + sigsetjmp recovery, so a naive debugger tracing the handler sees signal mechanics, not the state machine. The route buffer is the single mutable state; final memcmp vs D.
- Each op is invertible and none is self-indexing on the pair ops - required so the author can build the map by starting from D and applying the ops forward in reverse order to derive the correct plaintext route, then encrypt it with the CFB keystream. To author: pick route -> CFB -> apply 104 ops (from a fixed walk over the map you design) -> result must equal D; the walk/state chain/cells come from the map and header, and D is stored encrypted so the header can't leak it.
