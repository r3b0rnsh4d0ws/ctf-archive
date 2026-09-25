# bushbash strawberries (AES-CBC bit-flip) — SOLVED

## Flag
`bushbash{don't-b@sh-the-str4wberry-bUsh}`

## Challenge
- 340 pts Medium. "Mmmm, I'm addicted to these juicy strawberries... Too bad I don't have a premium membership..."
- `nc 34.40.133.67 6001`, files: message.ct (80B valid AES-CBC request), strawberryserver.py

## Vulnerability
AES-CBC malleability (bit-flip) + decryption oracle (server prints decrypted fields).

Message layout (plaintext, 64B): `t`(8) `n`(8) `u`(16) `i`(32=CHECK). In CBC, flipping ct_block0 XORs into pt_block1 (`u`) and garbles pt_block0 (`t`,`n`).

## Exploit
1. Send valid `message.ct`, read printed `u` = `000000000345f8d381aa95e4ef70279a`
2. `delta = u XOR PREMIUM_USER` (`000000000234f923643a9520ef762777`)
3. `ct0' = ct0 XOR delta` → pt1 = PREMIUM_USER, pt0 n becomes huge garbage → count > 2^32 → flag trigger
4. **Gotcha:** flag print has no `flush=True` → send one more valid request to flush stdout buffer → flag revealed

## Key takeaway
When a server echoes decrypted message fields, you have a decryption oracle — use CBC bit-flipping to forge records even without the key. Corrupted "previous" blocks are fine if their fields are unchecked.
