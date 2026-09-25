# SCAN2026 - Challenge #4 Flag 9 (BSC Mainnet, 275pts) — Most-setter-call C2 contract + interval stats

**Status: SOLVED**

**Flag:** `flag{0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468|37|6303|1164911}`

## Question
Among the 16 C2 contracts (deployer 0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46, nonces
0,2,4..28,39), which received the MOST setter (0x47064d6a) calls? For that contract report:
address, total in-window setter calls, MIN interval (s) and MAX interval (s) between
chronologically consecutive successful calls. Window: Mar 16 2026 → cutoff block 109839734
(ts 2026-07-13T23:59:59Z); exclude the deployment tx; same-block calls = 0s interval.

## Answer
- **Contract:** `0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468` — the SEED contract (deployer nonce 8),
  with **37** in-window successful setter calls (the max; next-highest is 6 for nonce 12).
- **MIN_INTERVAL_SECONDS = 6303** — between nonce 45 (block 91298828, 2026-04-08T07:47:36Z) and
  nonce 46 (block 91312818, 2026-04-08T09:32:39Z).
- **MAX_INTERVAL_SECONDS = 1164911** — between nonce 69 (block 106261368, 2026-06-25T08:28:45Z)
  and nonce 72 (block 108183070, 2026-07-05T08:46:43Z).

## Method
1. Reused the Flag 6 RPC-verified dataset `tx_verified.json` (105 deployer txs; from/to/input/
   block/nonce/status verified via `eth_getTransactionByHash` + `eth_getTransactionReceipt`).
   No new chain scanning needed — read-only reuse.
2. Extracted seed setter calls: `from == deployer`, `to == seed`, `input` starts `0x47064d6a`,
   `status == 0x1`, `block <= 109839734` → **37 txs**. (39 total seed setters; nonces 80 & 100
   are post-cutoff at blocks 110,676,870 / 112,217,780 and were excluded. No deployment tx is a
   setter — deployments carry init-code calldata `0x60a06040`.)
3. All 37 calls landed in 37 distinct blocks, so the "same block = 0s interval" rule never
   applied; ordering is purely by block.
4. Fetched each block's timestamp via `eth_getBlockByNumber` on the public BSC dataseed
   (`https://bsc-dataseed1.binance.org`, unauthenticated). All 37 fetched; a second pass over a
   subset returned identical values (self-verification).
5. Sorted chronologically, diffed consecutive timestamps → 36 intervals; `min=6303`,
   `max=1164911`. Sanity: sum of gaps = last_ts − first_ts = 10,172,601s ✓; first call ts
   1773668605 ≥ window start 1773619200 ✓, last call ts 1783841206 ≤ cutoff ts 1783987199 ✓.
6. Max-setter contract cross-checked against Flag 7 per-contract counts (seed=37; all others ≤6).

## Gotchas
- **Post-cutoff setter calls exist:** seed got 39 setters total; 2 (nonce 80, 100) are after the
  cutoff block. Only block-bounded counting gives 37.
- **Interval source of truth is the BLOCK timestamp**, not anything in the tx object (EVM txs have
  no timestamp; `eth_getBlockByNumber` is the way).
- **Same-block rule:** every call here was in its own block, so 0s never occurred; don't
  pre-assume the min is 0. Handle it as a general case (group by block → 0 gap) but verify.
- **RPC reliability:** BSC dataseeds are fast/unauthenticated for block metadata; ankr returned
  malformed responses and publicnode 403'd during this session — dataseed1 was dependable.
- Timestamps in-window check: use epoch [1773619200, 1783987199] AND block ≤ 109839734 (block
  bound is the binding one).

## Files
- Solvers: `C:\Users\balu\ctf-shared\scan2026\flag9_extract.py`, `flag9_ts.py`, `flag9_final.py`
- Data: `C:\Users\balu\ctf-shared\scan2026\flag9_seed_setters.json`, `flag9_block_ts.json`,
  `flag9_flag.txt`
- Source dataset: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#4-flag-6\tx_verified.json`
- Research: `D:\CTF\data\research\web3\scan2026_bsc_arb.md`
