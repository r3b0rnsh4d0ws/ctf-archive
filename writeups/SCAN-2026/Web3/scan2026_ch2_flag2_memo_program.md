# SCAN2026 Challenge #2 Flag 2 — Solana C2 memo program (75 pts)

**Date:** 2026-08-03 · **Category:** web3 / blockchain OSINT (Solana) · **Status: SOLVED**

## Flag
```
flag{MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr}
```

## Question
Seed address `28PKnu7RzizxBzFPoLp69HLXp9bJL3JFtT2s5QzHsEA2` is a malware C2 wallet.
"A Solana program is being used to write data into transactions." Submit the PROGRAM
ADDRESS as `flag{PROGRAM_ADDRESS}`.

## Answer
The **SPL Memo Program v2** at `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr`.
This is the program that writes the C2 data (base64 `{"link":...}` payloads) into the
seed's transactions.

## Evidence chain
1. **Pull txs** — `getSignaturesForAddress(seed, {limit:10})` against
   `https://api.mainnet-beta.solana.com` (Python urllib, retry/backoff for 429s).
2. **Decode txs** — `getTransaction(sig, {maxSupportedTransactionVersion:0})`;
   map `message.accountKeys` + `instructions[].programIdIndex` to program pubkeys.
3. **Program usage counts over 10 sampled txs:**
   - `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr` — **10/10 txs**
   - `11111111111111111111111111111111` (System Program) — 4/10 (fee payment only)
4. **Data-writing proof** — `meta.logMessages` of each tx:
   ```
   Program MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr invoke [1]
   Program log: Signed by 28PKnu7RzizxBzFPoLp69HLXp9bJL3JFtT2s5QzHsEA2
   Program log: Memo (len 59): "{\"link\":\"aHR0cDovLzEzNy4xODQuMTk4LjkxL1IyZElYQUpwU1h3eFA=\"}"
   ```
   The memo instruction data IS the C2 link payload (base64-encoded URL). Decoded sample:
   `aHR0cDovLzIxNy42OS4zLjUxL1lGeXEyNHRwVjVYM2FsOEN0aHBNcFElM0QlM0Q=`
   → `http://217.69.3.51/YFyq24tpV5X3al8CthpMpQ==`.
5. **Identity** — `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr` is the official SPL
   Memo Program v2 (stateless, writes arbitrary UTF-8 into tx data at zero cost;
   v1 is `Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo`). Perfect covert C2 channel.
6. **Cross-check with Flag 1** — Flag 1 progress already labeled these "Memo-program
   C2 broadcasts"; on-chain logs confirm 100%.

## Gotchas
- Instruction `data` field in `getTransaction` is base64 (versioned) / base58 (legacy);
  decoding it as UTF-8 gives binary garbage. Use `meta.logMessages` `Memo (len N): ...`
  lines for the clean payload text.
- Public mainnet RPC rate-limits per-method (~429) — retry with exponential backoff.
- Solscan API 403s scripted access; RPC is the reliable source.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\solve_c2f2.py` — RPC decode script
- `C:\Users\balu\ctf-shared\scan2026\flag2_scan.txt` — raw evidence (10 txs)
- `D:\CTF\ctfs\0_scan2026\challenges\challenge-#2-flag-2\progress.md`
- Research appended: `D:\CTF\data\research\osint\scan2026_explorers.md`
