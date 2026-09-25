# SCAN2026 — Challenge #4 Flag 8: Earliest incoming native BNB funding to deployer

**Category:** Web3 / BSC Mainnet · **Points:** 75 · **Status:** SOLVED

**Flag:** `flag{0xc44a7ddbbb2ef5c3e00ccc23fb2f98495f80d3b0|0x42e68ce143a0ba15742bcd2187dbdbe78181692393f22f4a44b38a0c50a3f32c|0.011547|2025-12-23T02:09:03Z}`

## Challenge
Among ALL successful top-level native-BNB transactions sent TO deployer
`0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46` with value > 0, from genesis through cutoff block
109839734 (no scenario-window start), submit the chronologically earliest:
funder address, tx hash, BNB amount (half-up to 6 decimals), UTC timestamp.

## Answer
| Field | Value |
|---|---|
| FUNDER_ADDRESS | `0xc44a7ddbbb2ef5c3e00ccc23fb2f98495f80d3b0` |
| TX_HASH | `0x42e68ce143a0ba15742bcd2187dbdbe78181692393f22f4a44b38a0c50a3f32c` |
| AMOUNT_BNB | `0.011547` (11546560212895441 wei = 0.011546560212895441 BNB) |
| TIMESTAMP_UTC | `2025-12-23T02:09:03Z` (block 72,604,985, ts 1766455743) |

Block 72,604,985 is well below the cutoff 109,839,734; receipt status `0x1` (success); input `0x`
(plain BNB transfer, no calldata).

## Method
1. **Reuse complete tx history (Flag 6).** Flag 6 had already scraped the deployer's full BscScan
   address page (`/txs?a={deployer}&p={n}`, 3 pages, 105 unique hashes) with pagination
   completeness proven by nonce 0..102 == `eth_getTransactionCount` (0x67 = 103). Of the 105 rows,
   exactly **2 are incoming** (from != deployer, to == deployer, input `0x`):
   - `0x42e68ce...` @ block 72,604,985 from `0xc44a7ddb...`
   - `0x0fda8f51...` @ block 86,937,608 from `0xe39d8fdc...`
2. **RPC-verify both candidates** (public BSC dataseeds, no key): `eth_getTransactionByHash`
   (from/to/value/input/blockNumber), `eth_getTransactionReceipt` (status), and
   `eth_getBlockByNumber(block)` (block timestamp). Both successful, value > 0, both <= cutoff.
3. **Earliest = min(blockNumber)** = `0x42e68ce...` @ 72,604,985.
4. **Amount:** value `0x2905890bde06d1` = 11546560212895441 wei = 0.011546560212895441 BNB.
   Half-up to 6 dp: `int(0.011546560212895441*1e6 + 0.5)/1e6 = 0.011547` (Python `round()` is
   banker's rounding — deliberately not used).
5. **Timestamp:** block 72,604,985 ts = 1766455743 = `2025-12-23T02:09:03Z`.
6. **Independent cross-check (BscScan HTML `/tx/0x42e68ce...`):** meta Description
   "Transfer 0.0115 BNB to 0x3a35b409...9b8dBDf46 | Success | Dec-23-2025 02:09:03 AM (UTC)",
   full-precision value span `0.011546560212895441 BNB`, sender `0xc44a7ddbbb2ef5c3e00ccc23fb2f98495f80d3b0`.
   RPC and explorer agree on every field.

## Gotchas
- "Top-level" = `to == deployer` in `eth_getTransactionByHash` (not an internal call).
- BscScan meta description truncates the amount to ~4-5 significant figures ("0.0115 BNB") — use
  the value span or RPC for full precision.
- Half-up rounding is NOT Python `round()` default (banker's rounding rounds .5 to even).
- Incoming txs carry no deployer nonce; completeness of the inbound set is proven by address-page
  pagination (row count = outgoing nonces + incoming).

## Files
- Solver: `flag8_solver.py` (RPC fetch of candidates + block timestamps)
- Data: `flag8_incoming.json` (RPC-verified values/timestamps)
- Research: `D:\CTF\data\research\web3\scan2026_bsc_arb.md`
