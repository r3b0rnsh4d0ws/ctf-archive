# SCAN2026 Challenge #7 - Flag 4 — Ronin Bridge USDC Laundering (275 pts)

## Challenge
Ronin Bridge exploiter `0x098B716B8Aaf21512996dC57EB0615e2383E2f96` received 25,500,000 USDC from the Ronin Bridge.
- Find the tx hash of the 25.5M USDC receipt.
- Find the 2 intermediary addresses the exploiter sent it to (across 5 outbound transfers).
- For each intermediary: which DEX router (To field of its OWN tx) did it call DIRECTLY?
- isBlacklisted() on USDC at snapshot block 25629979 (0x187151b) for each intermediary.
- Order groups ascending by intermediary (lowercase hex).

## Flag
```
flag{0xed2c72ef1a552ddaec6dd1f5cddf0b59a8f37f82bdda5257d9c7c37db7bb9b08|0x665660f65e94454a64b96693a67a41d440155617|Uniswap V3|false|0xe708f17240732bbfa1baa8513f66b665fbc7ce10|1inch|false}
```

## Solution walkthrough

### 1. Bridge tx (25.5M USDC receipt)
USDC contract `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`, Transfer event `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef`.
`eth_getLogs` topics `[TransferSig, null, to=exploiter]`, block range 14350000..14600000 (Ronin hack = 2022-03-23, ~block 14.44M) on archive-capable public RPC (mainnet.gateway.tenderly.co) → **one** log:
- tx `0xed2c72ef1a552ddaec6dd1f5cddf0b59a8f37f82bdda5257d9c7c37db7bb9b08`, block 14442840, 25,500,000 USDC, from `0x1A2a1c938CE3eC39b6D47113c7955bAa9DD454F2`.

That sender is **Ronin Bridge V1 (MainchainGatewayProxy)** per Blockscout; tx.to = same bridge, calldata 0x993e1c42 = `withdrawERC20For(uint256,address,address,uint256,bytes)` (4byte.directory id 233902). SolidityScan's Ronin Hack Analysis confirms this is "attacker's second transaction".

⚠️ Anti-trick: the challenge hint "Ronin bridge contract 0x2dccdb493827e15a5dc8f8b72147e6c4a5620857" is a **decoy** — that address is the **Harmony ERC20EthManager** (Horizon bridge), already handled in Flag 3. Trust on-chain Transfer logs.

### 2. Five outbound transfers → two intermediaries
`eth_getLogs` topics `[TransferSig, from=exploiter, null]`, block 14442840..14650000 → exactly 5:

| tx | block | to | USDC |
|----|-------|----|------|
| 0x55ae6a40fb41abe493f5f70bba0d6aa4386e2b082ad3ffc851bf22a3dfa7e9b | 14442948 | 0xe708f17240732bbfa1baa8513f66b665fbc7ce10 | 1,000,000 |
| 0x685e095d1f79f1f1af83cf2549a63857b25df28d5b316d514780a4a1c0ad4823 | 14442954 | 0x665660f65e94454a64b96693a67a41d440155617 | 1,000,000 |
| 0x4e6d5f19c5237caa30b947e2b6137fec1bb0cb89d11d97bbfeb625909b407680 | 14442976 | 0x665660f65e94454a64b96693a67a41d440155617 | 10,000,000 |
| 0xbb0c1380942c22799dea1df70cca4b4640f1f38760cb9dac9900d0d8099af7c1 | 14442981 | 0xe708f17240732bbfa1baa8513f66b665fbc7ce10 | 10,000,000 |
| 0x287dad48bfea44fcd5e180a9109e51e56bda64504d3242879c2575d83265c538 | 14442995 | 0x665660f65e94454a64b96693a67a41d440155617 | 3,500,000 |

- `0x665660f65e94454a64b96693a67a41d440155617` ← 14,500,000 USDC
- `0xe708f17240732bbfa1baa8513f66b665fbc7ce10` ← 11,000,000 USDC
Sum = 25.5M ✓ (both EOAs, per Blockscout)

### 3. Venues — the router each intermediary called DIRECTLY
Inspect each intermediary's own swap tx (`eth_getTransactionByHash`):

- `0x665660f6...`: 3 txs (0xbe0a102e…, 0xcedd0494…, 0x4f529a6f…) → `to = 0xE592427A0AEce92De3Edee1F18E0157C05861564`, input 0xac9650d8 (multicall) = **Uniswap V3 SwapRouter** (Blockscout verified). USDC logs from it go to pools 0x88e6a0c2….
- `0xe708f172...`: 3 txs (0x7f7a65ee…, 0x4e40f0b1…, 0x274e3a91…) → `to = 0x1111111254fb6c44bAC0beD2854e76F90643097d`, input 0x7c025200 (swap) = **1inch AggregationRouterV4** (Blockscout verified). Its USDC logs go to pools 0x220bda5c… / 0x2057cfb9… — those are the *settlement* pools, NOT the venue. The venue = the aggregator router itself.

### 4. Blacklist at snapshot block 25629979 (0x187151b, 2026-07-28T08:00:00Z)
`eth_call` `isBlacklisted(address)` (selector 0xfe575a87) on USDC proxy at blockTag `0x187151b`:
- `0x665660f6...` → 0x00 → **false** (tenderly, drpc, 1rpc all agree)
- `0xe708f172...` → 0x00 → **false** (same consensus)
- Control: exploiter at same block → 0x01 → **true** (was blacklisted 2022-03-24, block 14585983, tx 0xfa36edd16968a8a2e0a35a6131e97bd283ffd2def134c2f5b7b2cbabbd873d05 — AFTER laundering). Full-history Blacklisted-event scan (topic 0xffa4e618…) confirms the two intermediaries were NEVER blacklisted.

**Conclusion: Lazarus swapped the 25.5M USDC into ETH/tokens on Uniswap V3 + 1inch within ~3 minutes of receiving it — before Circle could freeze the intermediaries. The exploiter itself was frozen, the money was not.**

### 5. Ordering
Lowercase hex: `0x665660f6...` < `0xe708f172...` → group1 = 0x665660f6 (Uniswap V3, false), group2 = 0xe708f172 (1inch, false).

## Key takeaways / techniques
1. **Archive-capable public RPC for eth_getLogs**: publicnode/drpc/1rpc restrict ranges (50..10k blocks) or need tokens; `mainnet.gateway.tenderly.co` and `eth.drpc.org` (≤10k blocks) work for 2022-era logs.
2. **Topic indexing**: ERC-20 Transfer has `indexed from` (topics[1]) and `indexed to` (topics[2]); filter one side, decode the other from the topic.
3. **Venue = tx.to of the caller's own tx**, NOT the pools in the token-transfer logs (aggregator red-herring).
4. **Blacklisted event sig**: `Blacklisted(address)` = 0xffa4e6181777692565cf28528fc88fd1516ea86b56da075235fa575af6a4b855; `UnBlacklisted(address)` = 0x117e3210bb9aa7d9baff172026820255c6f6c30ba8999d1c2fd88e2848137c4e.
5. **Snapshot eth_call**: pass blockTag hex to get historical blacklist state; control-verify with a known-blacklisted address (the exploiter) at the same block.

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\flag4_solver.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#7-flag-4\progress.md`
- Research: `D:\CTF\data\research\osint\scan2026_explorers.md`
