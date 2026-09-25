# SCAN2026 — Challenge #6 Flag 1 (Ethereum Mainnet, 100 pts)

## Flag
```
flag{130}
```

## Challenge
Threat actor launders stolen funds through Tornado Cash (June 2024). Six listed depositing addresses. Sum total ETH deposited to the 4 TC pools (100/10/1/0.1 ETH denominations).

## Method
1. Pulled all transactions for the 6 depositing addresses (Blockscout `/addresses/{addr}/transactions`, full pagination), filtered to June 2024, outgoing, value>0.
2. **Key finding:** no direct transfers to the pools — every deposit went to the **Tornado relayer contract** `0xd90e2f925DA726b50C4Ed8D0Fb90AD053324F31b`.
3. Verified each deposit tx calldata: selector `0x13d98d13` (relayer deposit) with first arg = pool address `0x910cbd523d972eb0a6f4cae4618ad62622b39dbf` (the 10 ETH pool) + 32-byte commitment → confirms TC relayer deposit flow.
4. Deposit count per address (all exactly 10.0 ETH):
   - 0xD87786CA...: 2, 0x18Dd22d0...: 2, 0x32d2fDaE...: 2, 0xE938B5f9...: 2, 0x03eEa32d...: 2, **0x3BC3D3FA...: 3**
   - Total = **13 × 10 ETH = 130 ETH**

## Gotchas
- Deposits don't go pool-direct; they go through a relayer contract — count the value each depositing address sent for TC-deposit calls (parsed from calldata pool arg), don't require `tx.to == pool`.
- The 6 addresses also shuffle small non-denomination amounts between themselves (0.35–1.7 ETH) — exclude those.
- 0x3BC3D3FAD... made THREE deposits, not two (easy to miscount).

## Files
- Scripts: `C:\Users\balu\ctf-shared\scan2026\c6_tornado.py`, `c6_dump.py`, `c6_verify.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#6-flag-1\progress.md`
