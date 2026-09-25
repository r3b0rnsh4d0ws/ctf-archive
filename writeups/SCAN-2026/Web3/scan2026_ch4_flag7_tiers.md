# SCAN2026 — Challenge #4 Flag 7 (100 pts, BSC): Tier the 16 C2 contracts by setter call count

**Flag:** `flag{6|9|1}`

## Question
Categorize each of the 16 C2 contracts (deployer `0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46`,
CREATE-derived from nonces 0,2,4,...,28,39) by its in-window setter (`0x47064d6a`) call count:
- ACTIVE = ≥ 3 setter calls
- RESERVE = 1 or 2 setter calls
- DORMANT = 0 setter calls

Submit `flag{ACTIVE_COUNT|RESERVE_COUNT|DORMANT_COUNT}`.

## Answer
| Tier | Threshold | Count | Nonces |
|------|-----------|-------|--------|
| ACTIVE | ≥ 3 setters | **6** | 0, 6, 8, 12, 18, 20 |
| RESERVE | 1–2 setters | **9** | 2, 4, 10, 14, 16, 22, 24, 26, 28 |
| DORMANT | 0 setters | **1** | 39 |

`flag{6|9|1}` — 6 + 9 + 1 = 16 contracts; in-window setter sum = 37+6+3+3+3+3+9 = 64 (matches Flag 6).

## Method (read-only; reused Flag 6's RPC-verified dataset)

### 1. Data reuse
Flag 6 already scraped the deployer's full BscScan HTML txlist (keyless) and RPC-verified all
105 txs (`tx_verified.json`: from/to/input/block/nonce/status per tx via
`eth_getTransactionByHash` + `eth_getTransactionReceipt` on public BSC dataseeds).

### 2. Re-derivation from raw data (independent of Flag 6's summary)
For each tx in `tx_verified.json`, count it iff:
- `from == deployer`
- `to` in the 16-contract set
- `input` starts with `0x47064d6a` (setter selector)
- receipt `status == '0x1'` (success)
- `block <= 109839734` (cutoff; ts bound 1783987199 verified equivalent — see spot-check)

Per-contract in-window counts:
```
nonce 0   0xa6002d8c...  3   ACTIVE
nonce 2   0x2a9c2c7c...  1   RESERVE
nonce 4   0x77c08d8a...  1   RESERVE
nonce 6   0x6936edc5...  3   ACTIVE
nonce 8   0x7cc3cfc1... 37   ACTIVE  (seed)
nonce 10  0xff1cbfc9...  1   RESERVE
nonce 12  0xe9d1a9fb...  6   ACTIVE
nonce 14  0xea06a6ad...  1   RESERVE
nonce 16  0x5e801fcd...  1   RESERVE
nonce 18  0xb62b92c7...  3   ACTIVE
nonce 20  0x04985135...  3   ACTIVE
nonce 22  0xe4ae582b...  1   RESERVE
nonce 24  0xadfc3c72...  1   RESERVE
nonce 26  0x4dce5d54...  1   RESERVE
nonce 28  0xc5af7592...  1   RESERVE
nonce 39  0x96044f6d...  0   DORMANT
```

### 3. Independent live spot-checks (public RPC, read-only)
- `eth_getBlockByNumber(0x68c0576)` → timestamp `1783987199` = exactly 2026-07-13T23:59:59Z
  (cutoff boundary correct).
- `eth_getTransactionCount(deployer, 0x68c0576)` → `0x50` = **80** → nonces 0..79 pre-cutoff;
  the 6 setter txs excluded by the block filter (nonces 80, 98–102, blocks 110.6M–112.6M) are
  all post-cutoff. No in-window txs were dropped.

### 4. Tier tally
ACTIVE (≥3): nonces {0,6,8,12,18,20} = **6** · RESERVE (1–2): nonces
{2,4,10,14,16,22,24,26,28} = **9** · DORMANT (0): nonces {39} = **1**.

## Gotchas
- **Flag 6's informal note "1 each for 10 others" is imprecise** — exactly 9 contracts have 1
  setter; the nonce-39 contract has 0 and is DORMANT, not RESERVE. 6+9+1 = 16, never 17.
- Sanity: tier counts must sum to 16 and the weighted setter sum to 64 (Flag 6).
- Count granularity: 1 tx = 1 call to 1 contract (no multicall batching in this family).

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\flag7_tiers.py`
- Data: `challenge-#4-flag-6\tx_verified.json`, `challenge-#4-flag-6\contracts.json`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#4-flag-7\progress.md`
