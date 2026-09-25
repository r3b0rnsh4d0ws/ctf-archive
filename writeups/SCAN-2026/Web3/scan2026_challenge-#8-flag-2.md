# SCAN2026 — Challenge #8 Flag 2 (125 pts) — Swap count to 0x V4 router

## Flag
```
flag{3}
```

## Challenge
Seed `0xe8bde8169a2f6ed6855201afcac7be05a5639b25` laundered ~$27M over Aug 28–Sep 15 2024. Count how many individual swap transactions the seed sent to the 0x Protocol V4 router.

## Method
1. **Blockscout v1 `txlist`** for the seed (window blocks 20623368..20759464): 249 txs, exactly **3** to the real ExchangeProxy `0xdef1c0ded9bec7f1a1670819833240f027b25eff`, all calling `transformERC20` (`0x415565b0`):
   - `0xec4b9a7c...` (20626803) — USDT swap
   - `0x36a694d0...` (20626831) — USDC swap
   - `0x03d38dad...` (20628199) — USDT swap
2. **Receipt proof:** all 3 status=1 and emit `TransformedERC20` (topic0 `0x0f6672f78a59ba8e5e5b5d38df3ebc67f3c792e2c9259b8d97d7f00dd78ba1b3`) from the router with topic1 = seed.
3. Consistent with Flag 1 (2 USDT transfers + 1 USDC transfer = 3 token-transfer txs).

## Gotchas
- The brief's "router" `0xdef171fe48cf0115b1d80b88dc8eab59176fee57` is the 0x team Gnosis Safe — the real router is `0xdef1c0ded9bec7f1a1670819833240f027b25eff`. Count txs TO the real router.
- Count via txlist to router, not token-transfer events (one swap can move several tokens through the FlashWallet).

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\c8_flag2.py` (solver)
- `progress.md` (challenge dir)
