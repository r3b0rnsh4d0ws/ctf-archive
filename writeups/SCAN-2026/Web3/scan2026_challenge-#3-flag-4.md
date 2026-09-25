# SCAN2026 — Challenge #3 Flag 4 (150 pts) — Operator fee percentage per settlement tx

## Flag
```
flag{20%|25%|30%}
```

## Challenge
Drainer affiliate program — the operator charges AFFILIATES different commission tiers, not a flat rate. For each of the 3 settlement transactions, compute the operator fee %:
- Numerator = ETH received by operator revenue wallet `0x9fa7bb759641fcd37fe4ae41f725e0f653f2c726` in that tx
- Denominator = TOTAL ETH distributed by drainer `0x00000f312c54d0dd25888ee9cdc3dee988700000` in that tx
- % = num/den × 100, round half-up to nearest whole integer
- Submit 3 percentages in ASCENDING numeric order, pipe-separated.

Txs: A `0xefeba275...`, B `0x2e2af315...`, C `0x3752ca05...`

## Method
1. **Fetch fresh tx data** via `eth_getTransactionByHash` (RPC `https://eth.merkle.io`, keyless). All 3 txs: `from`=backend `0x63605e53...44a51`, `to`=drainer `0x00000f31...000`, input selector `0x065573f8` (`withdrawToBulk`).
2. **Decode the bulk-payout calldata** (authoritative — the drainer literally carries the payout list): `0x065573f8` + `0x20` (offset) + `len=3` + 3 × interleaved 32-byte `(address, amount)` words. Sum of all amounts = denominator (TOTAL ETH distributed). Amount to `0x9fa7bb...c726` = numerator.
3. **Compute % with exact rational arithmetic** (`Fraction`), round half-up (`floor(v+0.5)`).
4. **Cross-check denominator** via Blockscout v1 `txlistinternal` (`module=account&action=txlistinternal&txhash=`) — the internal CALL transfers out of the drainer match the calldata pairs wei-perfectly (3 transfers each).

## Results
| Tx | `0x9fa7bb...c726` (num) | total distributed (den) | % | half-up |
|---|---|---|---|---|
| A `0xefeba275...` blk 18325074 | 6.66492762 ETH | 33.32463811 ETH | 20.0000000000% | **20%** |
| B `0x2e2af315...` blk 17845210 | 13.34989010 ETH | 53.39956039 ETH | 25.0000000000% | **25%** |
| C `0x3752ca05...` blk 18030770 | 4.47292901 ETH | 14.90976337 ETH | 30.0000000000% | **30%** |

Ascending numeric order: 20% < 25% < 30% → `flag{20%|25%|30%}`.

Note: amounts were chosen by the operator to be exact round percentages (within 1 wei — e.g. tx A numerator is exactly `20·total − 20` wei → 19.999…% but rounds half-up to 20%). Commission tiers: 20% (seed), 25%, 30% — the operator's fee schedule escalates per settlement.

## Gotchas
- Python's built-in `round()` uses **banker's rounding** (half-to-even) — for half-up rounding of exact rationals use `int(v + 0.5)`.
- Denominator = SUM of all internal value transfers OUT of the drainer (includes the small relayer rebate to tx.from backend `0x63605e...`, 0.0024–0.0438 ETH) — not just the affiliate+operator.
- `debug_traceTransaction` callTracer on merkle/llamarpc/ankr/tenderly was rate-limited (429) on this run — calldata decode + Blockscout v1 internal-tx cross-check is the reliable keyless path (same conclusion as Flag 3).

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\flag4_compute.py` (solver: fetch + decode + exact Fraction + half-up + sort)
- `C:\Users\balu\ctf-shared\scan2026\flag4_trace_check.py` (debug_traceTransaction attempt — rate-limited, retained as fallback)
- `C:\Users\balu\ctf-shared\scan2026\flag4_bsck_check.py` (Blockscout v1 internal-tx cross-check)
- `progress.md` (challenge dir)
