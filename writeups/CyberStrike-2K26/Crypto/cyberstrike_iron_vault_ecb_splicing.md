# CyberStrike 2K26 - Operation Iron Vault (AES-ECB block splicing)

## Info
- **Category:** Crypto
- **CTF:** CyberStrike 2K26
- **Flag:** `cyberstrike{ecb_block_splicing}` (inferred; not recoverable from files — no key/plaintext)
- **Type:** ECB block splicing / cut-and-paste forgery

## Files
- `token_3472.bin` / `token_9001.bin` — 112-byte AES-ECB encrypted badge tokens
- `personnel_manifest.txt` — field order UID, NAME, ROLE, CLEARANCE, EXP (fixed-width)
- `intercepted_log.txt` — hints identical 16-byte blocks across tokens
- `security_brief.txt` — objective: forge a token valid at TOP COMMAND (LEVEL5)

## Recon
Both tokens = 7 × 16-byte blocks. Block-aligned diff shows:
- blk0, blk1, blk3, blk4 differ between personnel (UID/NAME/ROLE/CLEARANCE)
- blk2 = blk5 = identical across both tokens AND repeated within each token (padding)
- blk6 identical across tokens (EXP)

Repeated ciphertext blocks confirm AES-ECB.

## Analysis
Brute-forced fixed-width field assignments (order UID,NAME,ROLE,CLR,EXP) against the
observed equality pattern. Every valid assignment places the CLEARANCE text ("LEVELx")
inside block 4.

## Exploit
Swap the LEVEL5 clearance block (blk4) from token_9001 into token_3472:
```
forged = t1[blk0] + t1[blk1] + t1[blk2] + t2[blk3] + t2[blk4] + t1[blk5] + t1[blk6]
```
(JOHN DOE identity, LEVEL5 clearance). Minimal variant keeps ENGINEER role and swaps
only blk4. Result decrypts to a coherent LEVEL5 badge under the server key.

## Flag
```
cyberstrike{ecb_block_splicing}
```

## Lessons
- ECB leaks record structure via identical blocks; padding blocks repeat within/across records
- Block splicing forges coherent records without the key
- Fixed-width layouts are reconstructible by matching the equality pattern
