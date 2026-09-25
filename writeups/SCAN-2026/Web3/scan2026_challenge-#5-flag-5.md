# SCAN 2026 — Challenge #5 Flag 5 (150 pts) — Radiant Capital Oct 16 2024: chains drained + top assets

## Flag
```
flag{2|BTCB|WBTC|wstETH|WETH}
```

## Challenge
- **Category**: Web3 / Blockchain forensics (READ-ONLY, explorers + public RPC only)
- **Task**: Number of chains with COMPLETED pool drains (drain executed + proceeds to operator wallet), followed by the four ERC-20/BEP-20 tokens (native ETH/BNB excluded) with the HIGHEST total USD value received by the operator wallet, ranked by CoinGecko daily close 2024-10-16.
- **Answer format**: `flag{CHAINS|TOKEN|TOKEN|TOKEN|TOKEN}` (tokens any order)

## Answer
- **CHAINS** = `2` — **Arbitrum** and **BNB Chain**. Base and Ethereum did NOT have completed drains (backdoor `0x57ba8957...` had zero Oct-16 txs there).
- **TOP-4 TOKENS** (any order): **BTCB, WBTC, wstETH, WETH**

| token | chain(s) | amount received by operator | price (close 2024-10-16) | USD |
|-------|----------|----------------------------|--------------------------|-----|
| BTCB | BSC | 160.345736 | $67,057 | $10.75M |
| WBTC | ARB | 150.911538 | $66,852 | $10.09M |
| wstETH | ARB | 2,404.466150 | $3,070.48 | $7.38M |
| WETH | ARB 2,353.74 + BSC 470.43 | 2,824.175635 | $2,604.13 / $2,606.88 | $7.36M |
| WBNB (5th) | BSC | 8,469.861813 | $594.52 | $5.04M |
| GM (GMX V2, 6th) | ARB | 1,866,406.727 | $1.83/$1.47 | $3.14M |
| weETH (7th) | ARB | 980.256439 | ~$2,831 | $2.78M |
| ARB (8th) | ARB | 3,840,364.727 | $0.567707 | $2.18M |

Total ≈ **$51.0M** (public reporting: ~$50-51M across Arbitrum + BNB Chain).

## Background
Radiant Capital, Oct 16 2024: malware-infected dev wallets signed a Safe tx that
transferred PoolAddressesProvider ownership to attacker backdoor `0x57ba8957ed2ff2e7ae38f4935451e81ceeefbf5`,
then the LendingPool implementation was swapped and pools drained. Backdoor was pre-deployed
on 4 chains (ARB, BSC, BASE, ETH) but the drain executed on **only 2** (ARB + BSC).
Operator (deployer) wallet = `0x0629b1048298ae9deff0f4100a31967fb3f98962` (from Flag 3).

## Method (read-only)

### 1. Operator wallet + drain txs per chain
- Operator EOA (Flag 3) = `0x0629b10482...`. The drained pool tokens went DIRECTLY to it.
- **ARB drain** = Flag-4 takeover tx `0x7856552db409fe51...` (block 264477049, 2024-10-16 17:09:18Z):
  receipt contains **12 ERC-20 Transfer events → operator**: WBTC, ARB, USDe, WETH, weETH,
  GM×2 (GMX V2 "GMX Market" tokens `0x47c0312...` / `0x70d9558...`), USDC, USDT, wstETH, USDC.e, DAI.
- **BSC drain** = operator tx `0xd97b93f633aee356d992b49193e60a571b8c466bf46aaf072368f975dc11841c`
  (nonce 5, block ts 0x670ff3a4 = 2024-10-16 16:53:56Z — *before* the ARB tx), `to=` backdoor `0x57ba8957` on BSC:
  receipt = 12 logs, **6 Transfer events → operator**: WBNB 8,469.86, WETH(BSC) 470.43,
  USDC 303,590.14, USDT 451,482.02, BTCB 160.35, wBETH 220.69 (+BUSD 0).
  - BSC drainer `0xf0c0a1a1` (created Oct 2 test) had **0 txs on Oct 16** — drain went through the backdoor directly.
  - Operator's BSC nonces 6-24 (17:02-17:11Z) were post-drain movements (calls to token contracts = swaps/transfers out).
- **Base + ETH**: Blockscout v2 `GET /api/v2/addresses/{backdoor}/transactions` → **0 items** in Oct 15-21.
  Operator's Base/ETH Oct-16 txs were incoming consolidations (bridges/exchange withdrawals), not pool drains.

### 2. Token identification
- `eth_call` `symbol()`/`decimals()` on each token contract via public RPC (arb1.arbitrum.io, bsc-dataseed1.binance.org).

### 3. Pricing (CoinGecko daily close 2024-10-16 — key-gated, so substitute)
- CoinGecko `simple/price` (anon) works but is spot-only; `/coins/{id}/history` = 401 (key required).
- **DeFiLlama** `https://coins.llama.fi/prices/historical/2024-10-16/{chain}:{0xaddr}` — free, no key, per-address daily close. Timestamp can be date `YYYY-MM-DD` or epoch (1729036800 = 2024-10-17 00:00 UTC = close of Oct 16).
- Missing addresses (wstETH, USDT): query the L1 canonical addresses (`ethereum:0x7f39c581...` wstETH = $3,070.48, `ethereum:0xdac17f95...` USDT = $1).

### 4. Ranking
Sum per token symbol across chains, multiply by daily close, sort desc. Top 4 = BTCB, WBTC, wstETH, WETH.

## Gotchas
- CoinGecko API now 401/429 without a paid key — DeFiLlama `coins.llama.fi/prices/historical` is the reliable free per-address daily price source.
- BSC drain happened ~16:53Z, ARB drain ~17:09Z (BSC first).
- The two "GM" tokens in the ARB receipt are GMX V2 **market** tokens (WBTC-USDC / WETH-USDC GMX markets), symbol "GM" — not the GMX governance token. (Chainhint-style public reports mislabel these.)
- WBNB is a BEP-20 token (not native BNB), so it qualifies — but its $5.04M was below the $7.36M top-4 cutoff, so the exclude-native rule didn't change the answer.
- CoinGecko-close ordering robustness: BTCB/WBTC ~$10.1-10.8M, wstETH/WETH ~$7.3-7.4M, WBNB $5.0M — the top-4 set is stable to any realistic price-source variation.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\flag5_compute.py` — final ranking computation
- `C:\Users\balu\ctf-shared\scan2026\flag5_*.py` — receipts, BSC discovery, price fetch
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#5-flag-5\progress.md`
- Research: `D:\CTF\data\research\web3\scan2026_bsc_arb.md`
