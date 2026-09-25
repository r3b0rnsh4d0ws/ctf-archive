# SCAN2026 — Challenge #4 Flag 6 (300 pts, BSC): Count setter transactions

**Flag:** `flag{64}`

## Question
How many setter transactions (selector `0x47064d6a`) did the deployer
`0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46` send to its 16 C2 contracts combined within the
scenario window (2026-03-16 → cutoff block 109839734, ts 2026-07-13T23:59:59Z)? Count only
successful calls, excluding contract deployments.

## Answer
**64** successful setter txs (all 70 setters succeeded; 6 are post-cutoff).

## Method (read-only, keyless)

### 1. Contract address set (from Flag 4/5)
16 C2 contracts = CREATE-derived from deployer nonces 0,2,4,...,28,39
(`keccak256(rlp([deployer, nonce]))[12:]`, pure-Python RLP + pycryptodome keccak).

### 2. Full deployer tx list without API keys
- BscScan V1 `txlist` API: NOTOK ("deprecated V1 endpoint"); V2 needs paid key for BSC.
- `bsc.blockscout.com`: 404 on every route (instance not serving).
- **Working path:** scrape server-rendered `https://bscscan.com/txs?a={deployer}&p={n}`
  (browser UA). Got 105 unique hashes in 3 pages.
- 105 rows = 103 deployer-sent txs (nonces 0..102) + 2 incoming funding txs. Confirmed
  complete: `eth_getTransactionCount(deployer, 'latest')` = `0x67` = 103, nonces contiguous
  (0..102, no gaps).

### 3. RPC verification of every tx
For all 105: `eth_getTransactionByHash` (from/to/input/blockNumber/nonce) +
`eth_getTransactionReceipt` (status) on public BSC dataseeds
(bsc-dataseed1-4.binance.org, blastapi, ankr, publicnode — rotate + UA + retries).
Saved to `tx_verified.json`.

### 4. Filter
- `from == deployer`
- `input` starts with `0x47064d6a` (setter selector)
- `to` in the 16-contract set
- receipt `status == '0x1'` (success)
- block ≤ 109839734 AND block timestamp within [1773619200 (2026-03-16T00:00:00Z),
  1783987199 (2026-07-13T23:59:59Z)]
- exclude deployments: creation txs have `to == null` and init-code calldata
  (`0x60a06040`), never the setter selector → automatically excluded.

### 5. Result
- 70 setter txs total → **all status 0x1** (0 failures), **all to the 16 contracts**
  (0 to other addresses), 0 setter-typed deployments.
- 64 in-window (blocks 86,937,951 → 109,747,493).
- 6 excluded = post-cutoff: nonces 80, 98, 99, 100, 101, 102 at blocks
  110,676,870 → 112,605,098 (2026-07-18 → 07-28).

### 6. Cross-checks
- Per-contract BscScan `/txs?a={contract}` scrape counting "Set Data"-labeled rows from the
  deployer: 3+1+1+5+39+1+8+1+1+3+3+1+1+1+1+1+0 = **70** (matches RPC).
- In-window per contract: seed 37, 0xe9d1a9fb 6, 0xb62b92c7/0x6936edc5/0x04985135/0xa6002d8c
  3 each, ten others 1 each, nonce-39 contract (0x96044f6d) 0. Sum = 64.
- Nonce boundary: cutoff `eth_getTransactionCount` = 0x50 = 80 (nonces 0..79 pre-cutoff);
  the 6 excluded setter txs are exactly the post-cutoff ones.

## Gotchas
- **Window epoch trap:** 1742083200 = 2025-03-16 (off by one year!). Correct:
  2026-03-16T00:00:00Z = 1773619200; 2026-07-13T23:59:59Z = 1783987199. Verify with a UTC converter.
- Explorer "Method" labels ("Set Data") are hints — raw calldata via RPC is truth.
- Address txs pages list incoming + outgoing; filter `from` and use the RPC nonce count for
  completeness.

## Files
- Solver scripts: `C:\Users\balu\ctf-shared\scan2026\flag6_solver.py`,
  `flag6_verify.py`, `flag6_final.py`, `flag6_crosscheck.py`
- Data: `contracts.json`, `deployer_txlist.json`, `tx_verified.json`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#4-flag-6\progress.md`
