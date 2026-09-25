# SCAN2026 — Challenge #3 Flag 3 (125 pts) — Operator fee wallet (round-percentage split)

## Flag
```
flag{0x9fa7bb759641fcd37fe4ae41f725e0f653f2c726}
```

## Challenge
Drainer affiliate program (Apr 2023–Feb 2024). Affiliate address changes per drain; operator wallets recur. In the seed tx two NON-affiliate addresses receive ETH: one takes a clean ROUND PERCENTAGE of the total distributed (operator fee wallet), the other gets only a small relayer rebate (varies per tx). Submit the wallet that takes the round percentage. Compare 3 settlement txs (seed + `0x2e2af315...` + `0x3752ca05...`).

## Method
1. **Fetch + decode bulk-payout calldata.** All 3 txs: `from` = backend `0x63605e53d422c4f1ac0e01390ac59aaf84c44a51`, `to` = drainer `0x00000f312c54d0dd25888ee9cdc3dee988700000`, selector `0x065573f8` (`withdrawToBulk`), payload = `0x20, len=3, (addr,amount)×3` interleaved 32-byte words. `eth_getTransactionByHash` via `mainnet.gateway.tenderly.co` (keyless, reliable) gives `raw input`.
2. **Verify with internal trace.** `debug_traceTransaction` callTracer on `https://eth.merkle.io` — the 3 internal CALLs out of the drainer match the calldata pairs exactly (wei-perfect). Blockscout v2 `/internal-transactions` was again empty/524-timeout for these txs.
3. **Compute % of total distributed per tx:**

   | Tx | `0x9fa7bb...c726` | backend `0x63605e...44a51` | affiliate (changes each tx) |
   |---|---|---|---|
   | seed `0xefeba2...` | 6.6649 ETH → **20.0000%** | 0.002446 ETH (0.0073%) | `0x059f30bc...` 26.6573 ETH (79.9927%) |
   | `0x2e2af315...` | 13.3499 ETH → **25.0000%** | 0.008571 ETH (0.0161%) | `0xb837d59e...` 40.0411 ETH (74.9839%) |
   | `0x3752ca05...` | 4.4729 ETH → **30.0000%** | 0.043759 ETH (0.2935%) | `0x45e54386...` 10.3931 ETH (69.7065%) |

4. **Decision rule:** the recurring wallet taking an exact round % of the total (20% → 25% → 30%) = operator fee wallet = `0x9fa7bb759641fcd37fe4ae41f725e0f653f2c726`. The other non-affiliate recipient (tx.from backend) receives a small, non-round, varying rebate (0.0024/0.0086/0.0438 ETH) = relayer gas rebate, NOT the fee wallet.

## Gotchas
- Blockscout v2 internal-transactions for these drainer txs is empty/524 (not indexed). Two reliable substitutes: (a) ABI-decode the tx `raw_input` (the drainer's bulk-payout function carries the full payout list), (b) callTracer on a public RPC (`eth.merkle.io` worked keyless).
- Don't confuse the relayer rebate wallet (tx.from backend, tiny non-round amounts) with the operator fee wallet (round % of total).
- Affiliate identity varies (0x059f30bc / 0xb837d59e / 0x45e54386) — never assume it's fixed.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\decode_payouts.py` (solver, decodes withdrawToBulk calldata + prints %) — also usable for other settle txs
- `progress.md` (challenge dir)
