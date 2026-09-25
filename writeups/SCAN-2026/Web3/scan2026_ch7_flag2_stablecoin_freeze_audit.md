# SCAN2026 — Challenge #7 Flag 2 (200pts): Lazarus seed addresses stablecoin freeze audit

**Status:** SOLVED — 2026-08-02
**Category:** Web3 / Ethereum mainnet (read-only OSINT + archive eth_call)
**Snapshot block:** 25629979 (`0x187151B`), hash `0x939f304cd90d3ed64df89e28fe824a9449956bc109a7b8d392cac5c69f3f809d`, ts 2026-07-28T07:59:59Z

## Objective
For 5 Lazarus-group seed addresses, record USDT + USDC balance (÷10^6 human-readable) and
blacklist status at the fixed snapshot block, then emit the 20-field flag
(5 groups × USDT_BAL|USDC_BAL|USDT_FROZEN|USDC_FROZEN).

## Method (100% read-only, public RPCs)
1. **Block tag gotcha:** challenge text wrote the tag as `0x1871c33` — that hex decodes to
   25631795, NOT 25629979. Correct hex for 25629979 = **0x187151B**. Always re-derive
   dec→hex yourself and confirm with `eth_getBlockByNumber` (returned the exact metadata hash).
2. `eth_call` with `blockTag: "0x187151B"` on every address × 4 calls:
   - `balanceOf(address)` = `0x70a08231` on USDT `0xdAC17F958D2ee523a2206206994597C13D831ec7`
     and USDC proxy `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
   - USDT blacklist view = `0x59bf1abe` (`getBlackListStatus` / `isBlackListed` mapping view — same selector)
   - USDC `isBlacklisted(address)` = `0xfe575a87`
3. **RPC reliability for archive block-tagged calls (2026-08):**
   - `mainnet.gateway.tenderly.co` — full 20/20 calls
   - `eth-mainnet.public.blastapi.io` — full 20/20 calls
   - `eth.drpc.org` — 15/20, `1rpc.io/eth` + `eth.merkle.io` — partial
   - `ethereum-rpc.publicnode.com` — block fetch OK but eth_call → HTTP 403
   - `rpc.ankr.com/eth` (key-walled), `rpc.flashbots.net`, `blockpi public`, `llamarpc` (521) — dead
4. Every field cross-verified: full consensus across BlastAPI + Tenderly + drpc + 1rpc + merkle.
   Blacklist status also re-checked at `latest` block — identical (stable, as expected for sanctions).

## Results (block 25629979)
| # | Address (seed) | USDT raw | USDT | USDC raw | USDC | USDT_FROZEN | USDC_FROZEN |
|---|----------------|----------|------|----------|------|-------------|-------------|
| 1 | 0x098B716B8Aaf21512996dC57EB0615e2383E2f96 (Ronin Exploiter) | 0x0 | 0 | 0x0 | 0 | true | true |
| 2 | 0x0d043128146654C7683Fbf30ac98D7B2285DeD00 (Harmony Exploiter) | 0x0 | 0 | 0x0 | 0 | false | false |
| 3 | 0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1 (Lazarus intermediary) | 0x0 | 0 | 0x0 | 0 | true | true |
| 4 | 0x47666Fab8bd0Ac7003bce3f5C3585383F09486E2 (ByBit Exploiter) | 0x55d4a80 | **90** | 0x2710 | **0.01** | false | false |
| 5 | 0x3130662aece32f05753d00a7b95c0444150bcd3c (Stake.com Exploiter) | 0x0 | 0 | 0x0 | 0 | false | false |

Conversions: `0x55d4a80` = 90,000,000 / 1e6 = **90**; `0x2710` = 10,000 / 1e6 = **0.01**. All others 0x0 → **0**.

Key observations:
- Only 2 of 5 seeds frozen by BOTH issuers at snapshot (Ronin + Lazarus intermediary).
- ByBit exploiter still holds live USDT 90 / USDC 0.01 and is NOT frozen — matches the
  real-world story where the ByBit stash kept moving before freeze actions.
- Harmony + Stake.com exploiters: zero balances and NOT blacklisted at snapshot.

## Flag
```
flag{0|0|true|true|0|0|false|false|0|0|true|true|90|0.01|false|false|0|0|false|false}
```

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\query_balances.py` (eth_call + flag builder)
- Cross-check: `C:\Users\balu\ctf-shared\scan2026\verify_cross_rpc.py` (multi-RPC consensus)
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#7-flag-2\progress.md`
- Research: `D:\CTF\data\research\osint\scan2026_explorers.md` (appended snapshot-audit section)
