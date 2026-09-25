# SCAN2026 — Challenge #8 Flag 1 (Ethereum Mainnet, 75 pts)

## Flag
```
flag{USDT|3540468975279|USDC|1116738659047}
```

## Challenge
~$27M laundered from seed `0xe8bde8169a2f6ed6855201afcac7be05a5639b25`, Aug 28–Sep 15 2024. Which stablecoins (USDT/USDC) did the seed send to the 0x Protocol V4 swap router, in raw 6-decimal amounts? List descending by amount.

## Method
1. Window blocks: 20623367 (Aug 28 00:00 UTC) – 20759464 (Sep 16 00:00 UTC), binary-searched via eth_getBlockByNumber timestamps.
2. eth_getLogs(Transfer, topics=[Transfer, seed]) for USDT and USDC over the full window (Tenderly gateway; drpc 10k-block chunks as fallback) → exactly 3 outbound stablecoin logs from the seed:
   - tx `0xec4b9a7c...` → USDT 1,477,594,675,912
   - tx `0x03d38dad...` → USDT 2,062,874,299,367
   - tx `0x36a694d0...` → USDC 1,116,738,659,047
3. All 3 txs have `tx.from = seed` and `tx.to = 0xdef1c0ded9bec7f1a1670819833240f027b25eff` — the **0x ExchangeProxy (V4 swap router)**, selector `0x415565b0`. Token transfers land in 0x **FlashWallet** `0x22f9dcf4647084d6c31b2765f6910cd85c178c18` (deployed by the ExchangeProxy). Receipts emit `TransformedERC20` (0x0f6672f7...) from the router → confirms 0x swap flow.
4. Totals: **USDT = 3,540,468,975,279** (largest), **USDC = 1,116,738,659,047** → flag in descending order.

## Gotchas
- The brief names `0xdef171fe48cf0115b1d80b88dc8eab59176fee57` as the "0x V4 swap router" — that address is actually the **0x team Gnosis Safe** (selectors 0x9010d07c/0xa64b6e5f). The router actually used by the seed is `0xdef1c0ded9bec7f1a1670819833240f027b25eff`. Always trust the on-chain tx targets over brief addresses.
- Stablecoin recipients are 0x FlashWallets (one per swap), not the router itself — filter by the enclosing `tx.to == router` (or by seed as Transfer sender within the window).
- All activity happened on Aug 28; the rest of the two weeks is ETH → exchanges.

## Files
- Scripts: `C:\Users\balu\ctf-shared\scan2026\c8_stable.py`, `c8_logs.py`, `c8_logs2.py`, `getlogs.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#8-flag-1\progress.md`
