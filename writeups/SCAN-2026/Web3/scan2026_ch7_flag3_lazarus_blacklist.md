# SCAN2026 Challenge #7 — Flag 3 (225 pts): Lazarus stablecoin transfers & blacklist

**Status: SOLVED** — 2026-08-02
**Category:** Blockchain tracing / OSINT (on-chain, READ-ONLY)
**Flag:** `flag{0x9e91ae672e7f7330fc6b9bab9c259bd94cd08715|USDT|false|0x9e91ae672e7f7330fc6b9bab9c259bd94cd08715|USDT|false|0x0d043128146654c7683fbf30ac98d7b2285ded00|USDC|false}`

## Objective
For 3 transactions attributed to the Lazarus group, determine per tx: (a) receiving address,
(b) asset transferred, (c) whether the receiving address was blacklisted at the fixed snapshot
block **25629979** (`0x187151B`, ts 2026-07-28T07:59:59Z).

## Result table

| # | Tx hash | Asset | Receiving address (ERC-20 recipient) | Amount | Blacklisted @snap |
|---|---------|-------|--------------------------------------|--------|-------------------|
| 1 | `0xf32d4cc531ec23576110833b9f04163c70a30ca21b7851ccc7a26eca79ea4c34` | USDT | `0x9e91ae672e7f7330fc6b9bab9c259bd94cd08715` | 4,981,000 | **false** |
| 2 | `0x618a7d833ea6f17cc7d762237d223d2285454d331b37bb499d3cef9ec7ce2417` | USDT | `0x9e91ae672e7f7330fc6b9bab9c259bd94cd08715` | 5,000,000 | **false** |
| 3 | `0x6e5251068aa99613366fd707f3ed99ce1cb7ffdea05b94568e6af4f460cecd65` | USDC | `0x0d043128146654C7683Fbf30ac98D7B2285DeD00` | 41,200,000 | **false** |

## Method
1. **Fetch** `eth_getTransactionByHash` + `eth_getTransactionReceipt` from public RPCs
   (drpc, blastapi, merkle, publicnode; ankr/llamarpc/flashbots were blocked in this run).
2. **Decode:**
   - TX1/TX2: `to` = USDT contract `0xdac17F958D2ee523a2206206994597C13D831ec7`,
     calldata selector `0xa9059cbb` (transfer) → recipient `0x9e91ae…`; confirmed by
     Transfer log topics[2]. Sender = Harmony Bridge Exploiter seed `0x0d0431…`.
   - TX3: `to` = multisig `0x715cdda5e9ad30a0ced14940f9997ee611496de6`,
     selector `0xc01a8c84` = `confirmTransaction(uint256 0x5273)`; the receipt's USDC
     Transfer log shows the asset leaving the **Harmony bridge contract**
     `0x2dccdb493827e15a5dc8f8b72147e6c4a5620857` (OKLink tag "Harmony") to
     `0x0d0431…` = 41,200,000 USDC (the Harmony Bridge Exploiter seed).
3. **Asset symbols** verified with `symbol()` on both contracts → "USDT"/"USDC".
4. **Blacklist check** (READ-ONLY `eth_call` at blockTag `0x187151B`):
   - `0x59bf1abe` = USDT `getBlackListStatus/isBlackListed(address)` → **0x00** (false) on 0x9e91ae…
   - `0xfe575a87` = USDC `isBlacklisted(address)` → **0x00** (false) on 0x0d0431…
   - Cross-checked both tokens on both addresses + at latest block → all false.
5. **Control validation** at the SAME snapshot block: USDT+USDC both return **true** for the
   Ronin Exploiter seed `0x098b…` and Lazarus intermediary `0x53b6…` → proves the calls are
   correct and the two recipients genuinely were not blacklisted at the snapshot.

## Gotchas / learnings
- **Receiving address = ERC-20 recipient (Transfer log topics[2])**, not the tx `to`
  (which is the token contract or a multisig). Use `eth_getTransactionReceipt` logs.
- TX1 & TX2 both send USDT to the **same** recipient `0x9e91ae…` (4.981M + 5M).
- Public RPCs are heavily rate-limited; rotate drpc/blastapi/merkle and add retries.
  publicnode eth_call 403s once you hit the limit; keep UA header set.
- Blacklist state at snapshot is authoritative; also cross-check "latest" to detect changes.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\scan2026_solve.py` (reproducible solver)
- `D:\CTF\ctfs\0_scan2026\challenges\challenge-#7-flag-3\progress.md`
- Research appended: `D:\CTF\data\research\osint\scan2026_explorers.md`
