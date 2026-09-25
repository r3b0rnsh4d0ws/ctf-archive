# SCAN2026 — Challenge #3 Flag 2 (125 pts) — Affiliate wallet & revenue split

## Flag
```
flag{0x059f30bc3ce1f7e8b68257dd11ad0e6c35d299d4|80%}
```

## Challenge
Wallet-drainer affiliate program. From seed tx `0xefeba2755c3cfbb4ddb48ab5d5705ec17256abfc3d19c1ee7f89489d00735464`, the drainer `0x00000f312c54d0dd25888ee9cdc3dee988700000` splits ETH between affiliate (largest recipient) and operator. Report affiliate address + its share % (denominator = all internal ETH out of drainer; round half-up).

## Method
1. **Decode the bulk-payout calldata.** Blockscout v2 tx view shows method `withdrawToBulk` (selector `0x065573f8`). The `raw_input` ABI-decodes to `[(addr, uint256)] × 3` — the drainer's payout list:
   | Recipient | wei | ETH |
   |---|---|---|
   | `0x059f30bc3ce1f7e8b68257dd11ad0e6c35d299d4` | 26,657,264,535,140,402,623 | 26.6573 ← **AFFILIATE (largest)** |
   | `0x63605e53d422c4f1ac0e01390ac59aaf84c44a51` | 2,445,949,759,503,731 | 0.00245 (operator backend, tx.from) |
   | `0x9fa7bb759641fcd37fe4ae41f725e0f653f2c726` | 6,664,927,621,224,976,588 | 6.6649 |
2. **Verify internally.** Blockscout v2 `/internal-transactions` returns empty (not indexed). Cross-check with Blockscout **v1** `txlistinternal` → identical 3 transfers, `from` = drainer, exact wei, `isError=0`.
3. **Compute.** Total = 33,324,638,106,124,882,942 wei. Percent = 26,657,264,535,140,402,623 / 33,324,638,106,124,882,942 × 100 = 79.99266% → **80%**.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\c3_flag2.py` (solver)
- `progress.md` (challenge dir)
