# SCAN2026 — Challenge #8 Flag 5 (275pts): eXch BTC payout for the 1000 ETH deposit

**Status:** SOLVED —
`flag{9458b472c23bc87382465304332380ad89c444e36e495f63820327f445ae2e77|4069402167|3HNhmWp4JspsKWBZ9USW3tEabBNYavytek|2089}`

## Challenge
Seed `0xe8bde8169a2f6ed6855201afcac7be05a5639b25` laundered ~$27M via eXch.cx (Aug 28–Sep 15 2024).
The 1000 ETH deposit occurred at 2024-09-09T00:36:35Z. Find the corresponding eXch BTC payout
(same method as Flag 4): `flag{BTC_TXID|AMOUNT_SATOSHIS|RECIPIENT_ADDRESS|SECONDS_AFTER_DEPOSIT}`.

## Answer components
| Field | Value |
|-------|-------|
| BTC_TXID | `9458b472c23bc87382465304332380ad89c444e36e495f63820327f445ae2e77` |
| AMOUNT_SATOSHIS | `4069402167` (40.69402167 BTC) |
| RECIPIENT_ADDRESS | `3HNhmWp4JspsKWBZ9USW3tEabBNYavytek` (P2SH legacy, case-sensitive) |
| SECONDS_AFTER_DEPOSIT | `2089` (01:11:24Z − 00:36:35Z) |

## Method
1. **Deposit anchor (Flag 3):** 1000 ETH deposit = tx `0x9f2bb5d58d5c5448b35e666df2f17ebac142865754f2106491879c5ea8d50cf4`
   → one-time deposit address `0x693eE0b5e0D588b2F9252c1b15B0e64d221962bD`, timestamp
   **2024-09-09T00:36:35.000000Z** (block 20709509, epoch 1725842195) — re-verified via Blockscout v2.
2. **Expected payout time:** Flag 4's correlation table already predicted delta 2089 s →
   payout block_time = 1725844284 (2024-09-09T01:11:24Z). Walked block heights with
   blockstream.info (`/block-height/{h}` → `/block/{hash}`) and converged to **block 860544**
   whose header timestamp is EXACTLY 1725844284.
3. **One-call block scan:** `https://blockchain.info/block-height/860544?format=json` returns all
   4226 txs of the block. Filtered for txs with an input from eXch's BTC hot wallet
   `bc1qu2dq8w8lv8v3l7lr2c5tvx3yltv22r3nhkx7w0` (aggregated pool, from eXch's own FAQ) →
   exactly ONE: tx `9458b472c2...` with 6 hot-wallet inputs (42.49575671 BTC) →
   **4,069,402,167 sats** to `3HNhmWp4JspsKWBZ9USW3tEabBNYavytek` + 180,172,311 sats change → HW.
4. **Uniqueness:** blocks 860543 (01:01:17Z) and 860545 (01:19:17Z) contain zero hot-wallet
   payouts → the 860544 tx is the unique match in the 5–45 min window.
5. **Recipient profile:** `3HNhmWp4JspsKWBZ9USW3tEabBNYavytek` (P2SH) funded exactly once
   (total_received = 4,069,402,167, n_tx=2), swept 100% at ~01:15:01Z (tx `07967cb7...`) — same
   fresh-per-order address pattern as Flag 4.
6. **Amount sanity:** 1000 ETH × ~$2,500 / ~$61K ≈ 40.9 BTC ✓ (eXch ~1% fee included).

## Gotchas / anti-tricks
- **blockchain.info tx `time` ≠ block header time:** for this tx blockchain.info reported
  1725842313 (00:38:33Z) but block 860544's header timestamp is 1725844284 (01:11:24Z). Always
  use the block header timestamp (blockstream/mempool `status.block_time`, or the `time` field of
  the block object from blockchain.info) — same trap as Flag 4.
- **No need to re-paginate the 15,600-tx wallet cache:** the Flag 4 correlation already gives the
  predicted delta; jump straight to the target block by height and scan it in one blockchain.info
  call. Great when blockstream is rate-limiting (429).
- **Recipient format varies:** Flag 4 recipient was bech32 (`bc1q...`), this one is P2SH legacy
  (`3...`, mixed case). Always read the actual address from the vout — do not assume bech32.
- Customer output = non-hot-wallet vout; hot wallet keeps the change (1.80 BTC here).

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\c8f5_solve.py`
- Verify: `C:\Users\balu\ctf-shared\scan2026\c8f5_verify2.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#8-flag-5\progress.md`
