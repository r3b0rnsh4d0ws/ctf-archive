# SCAN2026 — Challenge #8 Flag 4 (275pts): eXch BTC payout for the first 250 ETH deposit

**Status:** SOLVED — `flag{5a48761a5d65bf8f0eaf20bcb83b53d6957eb4edf3d00c49407e3306aa98253a|1033479062|bc1qsalmq8mkzaqp9dpnqt0vexxq2jy9u9572k9rl9|736}`

## Challenge
Seed `0xe8bde8169a2f6ed6855201afcac7be05a5639b25` laundered ~$27M via eXch.cx (Aug 28–Sep 15 2024).
First eXch deposit = 250 ETH at 2024-08-30T19:13:59Z (tx `0x4c7f90ed...`, to one-time deposit
address `0xE973D58f90da0F681c4727b5E513dC6A9AF6503c`). eXch swaps in 5–45 min. Find the BTC
payout: `flag{BTC_TXID|AMOUNT_SATOSHIS|RECIPIENT_ADDRESS|SECONDS_AFTER_DEPOSIT}`.

## Answer components
| Field | Value |
|-------|-------|
| BTC_TXID | `5a48761a5d65bf8f0eaf20bcb83b53d6957eb4edf3d00c49407e3306aa98253a` |
| AMOUNT_SATOSHIS | `1033479062` (10.33479062 BTC) |
| RECIPIENT_ADDRESS | `bc1qsalmq8mkzaqp9dpnqt0vexxq2jy9u9572k9rl9` |
| SECONDS_AFTER_DEPOSIT | `736` (19:26:15Z − 19:13:59Z) |

## Method
1. **Identify eXch's BTC hot wallet.** eXch's own FAQ (Wayback capture of `exch.cx/faq`,
   2024-09-07) explains they run TWO BTC pools: a **"mixed pool"** (per-order fresh addresses,
   untraceable) and an **"aggregated pool"** — a single known address that both receives customer
   BTC and sends payouts, deliberately published so chain-analysis platforms tag it as an exchange.
   The FAQ page contains the aggregated-pool address `bc1qu2dq8w8lv8v3l7lr2c5tvx3yltv22r3nhkx7w0`.
   (Cross-check: fable/nta.sy "Investigating eXch" 2024-10-06 confirms the modern eXch infra; the
   ETH hot wallet `0xf1dA173228fcf015F43f3eA15aBBB51f0d8f1123` from Flag 3 belongs to the same ops.)
2. **Enumerate hot-wallet txs.** Paginate `https://mempool.space/api/address/{HW}/txs` (and
   blockstream `/txs/chain/{last}`) back to Aug 30 2024 (15,600 txs cached). The wallet is a
   classic hot wallet: dozens of small payout txs/day with change-return patterns.
3. **Window filter.** In [deposit_epoch .. +1h] the ONLY non-change output of significant size is
   block 859123 / block_time **1725045975 (2024-08-30T19:26:15Z)**, tx `5a48761a...`:
   4 inputs from the hot wallet (10.76999903 BTC) → `1,033,479,062 sats` to
   `bc1qsalmq8mkzaqp9dpnqt0vexxq2jy9u9572k9rl9` + 43,519,096 sats change back to hot wallet.
4. **Amount sanity.** 250 ETH × ~$2,500/ETH ≈ $625K ≈ 10.33 BTC × ~$60K/BTC. eXch fee ≈ 1%.
   Delta = 736 s (12.3 min) — inside 5–45 min.
5. **Recipient profile.** `bc1qsalmq8...` is a fresh bech32 P2WPKH address: funded exactly once
   (chain_stats funded_txo_count=1, sum=1,033,479,062), swept 100% 38 min later to a legacy P2SH
   `39P3pUnZhqd6ho9Zk7uijfBMrrxAKesR6j` (2.0 BTC) + `bc1qtwy4dcexutz7w54ue08w2jvu5nw2nnwe3vqvvx`
   (8.33478 BTC). Consistent with drainer ops using a fresh BTC address per eXch order.
6. **Pattern validation.** Correlating all 12 deposits against aggregated-pool payouts in
   +5..45 min gives exact matches for 4 of them (250→10.335, 1000→40.694, 1008→40.990,
   277→11.099 BTC) — the first deposit's match is unambiguous and exact. The others were likely
   paid via the mixed pool (per-order fresh addresses).

## Gotchas / anti-tricks
- **Two BTC pools:** aggregated (linkable hot wallet, published by eXch) vs mixed (fresh per-order
  addresses). Don't assume every payout comes from the hot wallet.
- **Timing anchor:** the deposit-address → ETH-hot-wallet sweep (19:44:59Z) happens AFTER the BTC
  payout (19:26:15Z). eXch pays out on deposit-address confirmation (their FAQ: "Once you transfer
  the required amount to it and it gets confirmed, you will receive the cryptocurrency purchased").
  Measure deltas from the seed→deposit-address tx, not the hot-wallet receipt.
- **blockchain.info API `time` ≠ block time:** for this tx it reported 19:15:41 while the block
  header timestamp is 19:26:15. Use blockstream/mempool `status.block_time` (authoritative).
- **Identify the customer output:** in a payout tx the customer output is the NON-hot-wallet output
  (the hot wallet keeps change). Recipient = fresh address with single funding.

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\c8f4_solve.py` (keyless, self-verifying)
- Supporting scripts: `exch_pages.py` (FAQ hot-wallet extraction), `btc_window.py`,
  `btc_verify_tx.py`, `find_exch_btc*.py`; cache `exch_btc_txs2.json`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#8-flag-4\progress.md`
