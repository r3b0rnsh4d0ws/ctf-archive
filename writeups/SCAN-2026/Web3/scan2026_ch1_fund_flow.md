# SCAN2026 — Challenge #1 Flag 1 (Ethereum Mainnet, 100 pts)

## Flag
```
flag{0x0e05aec89abf3ca6abcfa060edd21db7d846e7b8|0x1c6e28d3f5175e9093de62a188d87c5ba8148b4d|0xdac17f958d2ee523a2206206994597c13d831ec7|0xf600c14e09c8997851b732d079d3b8e7b357980b|301665542644}
```

## Challenge
Deterministic fund-flow reconstruction from phishing seed A0=`0x560471559662903b1287ecff58909bc35bd7a59e`, blocks 15449618–15649594 (Sept 2022). Compute H1 (greatest EOA recipient of direct ETH from A0), H2 (same from H1, excl. A0/H1), token T (valid Transfer logs where H2 is sender/recipient; eligible if IN_T==OUT_T and IN_T>300000*10^d), C (greatest outgoing EOA recipient), TOTAL_RAW=IN_T.

## Method
1. **A0 history** (Blockscout `/addresses/{A0}/transactions`): A0 is a phishing deposit EOA — victims sent ~80 txs of 0.5–5 ETH on 2022-09-15; A0 forwarded to 2 EOAs. Verified each A0-out tx via RPC: from=A0, to!=null, value>0, input=="0x", receipt status=1.
   - H1 = `0x0e05aec89abf3ca6abcfa060edd21db7d846e7b8` (146.433 + 16.305 = **162.74 ETH**), EOA at end block 15649594
   - (other: `0x1c6e28...` 2.53 ETH)
2. **H1 history**: 4 direct transfers in scope → H2 = `0x1c6e28d3f5175e9093de62a188d87c5ba8148b4d` (187 + 0.67 + 0.516 = **188.19 ETH**), EOA at end block. (other: `0x9bb690...` 10.93 ETH)
3. **Token U**: eth_getLogs(Transfer, topics=[topic0, h2] and [topic0, null, h2]) over full range via Tenderly (drpc 10k-chunk fallback) → **only USDT** `0xdac17f958d2ee523a2206206994597c13d831ec7` (11 recipient logs + 4 sender logs). Cross-checked identical with Blockscout token-transfers (sources: Uniswap V3 pools 0x3416cf6c70, 0x11b815efb8, 0xac9c109128).
4. **IN/OUT** (validated: 3 topics, 32-byte data, status=1, no zero-address, no self, dedup): IN_T = OUT_T = **301,665,542,644**. decimals()@15649594 = 6. 301,665,542,644 > 300,000×10^6 → eligible.
5. Only eligible token → **T = USDT**, **TOTAL_RAW = 301665542644**.
6. **C**: all 4 OUT logs go to single EOA `0xf600c14e09c8997851b732d079d3b8e7b357980b` (301,665,542,644) → **C**.

## Files
- Scripts: `C:\Users\balu\ctf-shared\scan2026\c1_*.py` + `c1_logs_sender.json`, `c1_logs_recip.json`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#1-flag-1\progress.md`
