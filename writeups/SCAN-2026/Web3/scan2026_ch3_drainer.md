# SCAN2026 — Challenge #3 Flag 1 (Ethereum Mainnet, 100 pts)

## Flag
```
flag{0x00000f312c54d0dd25888ee9cdc3dee988700000}
```

## Challenge
Wallet-drainer-as-a-service affiliate program, window Apr 2023–Feb 2024. Seed tx `0xefeba2755c3cfbb4ddb48ab5d5705ec17256abfc3d19c1ee7f89489d00735464` distributes ~33.3 ETH. Find the drainer contract = sender of every distribution, with a distinctive vanity address.

## Method
1. `eth_getTransactionByHash` on seed tx: from=`0x63605e53d422c4f1ac0e01390ac59aaf84c44a51` (EOA operator backend), to=`0x00000f312c54d0dd25888ee9cdc3dee988700000`, value=0, input selector `0x065573f8`, block 18325074.
2. `eth_getCode(to)` at block → runtime bytecode → **`to` is a contract** with vanity address pattern `0x00000f31...000` (the drainer family marker).
3. Confirmed via Blockscout `/api/v2/transactions/{tx}/internal-transactions`: the contract is the sender of ALL distributions:
   - → 0x9fa7bb...c726: 6.6649 ETH
   - → 0x63605e...44a51: 0.0024 ETH (operator)
   - → 0x059f30...99d4: 26.6572 ETH (affiliate)
   - **Total = 33.3246 ETH ≈ 33.3 ETH** (matches brief exactly)

## Gotcha
Do not submit the EOA `tx.from` (operator backend) — the "sender of every distribution" is the contract `tx.to`, which is where the split happens. Verify with internal txs + getCode.

## Files
- Scripts: `C:\Users\balu\ctf-shared\scan2026\c3_probe.py`, `c3_trace.py`, `c3_internal.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#3-flag-1\progress.md`
