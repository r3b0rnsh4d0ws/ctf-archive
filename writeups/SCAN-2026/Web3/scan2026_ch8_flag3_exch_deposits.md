# SCAN2026 — Challenge #8 Flag 3: ETH transfers seed → eXch.cx deposit addresses

**Category:** Web3 / Ethereum Mainnet
**Points:** 150
**Flag:** `flag{12|8116000000000000000000|0x4c7f90edf99337fbbece710ffc00cef13de9a6fc8afc4784d70a48e0c917d277|0x8951d78536d2a4eac4be350d5834013b8cf901b1e3748f82165d3d2091ab8513}`

## Challenge
Seed `0xe8bde8169a2f6ed6855201afcac7be05a5639b25` laundered ~$27M over Aug 28–Sep 15 2024 via DEX swaps
(0x router), no-KYC exchanges (eXch.cx) and a secondary relay. Find ALL ETH transfers from the seed to
eXch.cx **deposit addresses** in the window → COUNT|TOTAL_WEI|FIRST_TX_HASH|LAST_TX_HASH (chronological).

## Answer
| field | value |
|-------|-------|
| COUNT | 12 |
| TOTAL_WEI | 8116000000000000000000 (8116 ETH) |
| FIRST_TX_HASH | 0x4c7f90edf99337fbbece710ffc00cef13de9a6fc8afc4784d70a48e0c917d277 (2024-08-30) |
| LAST_TX_HASH | 0x8951d78536d2a4eac4be350d5834013b8cf901b1e3748f82165d3d2091ab8513 (2024-09-10) |

## Method (read-only, keyless)

### 1. Identify the eXch.cx hot wallet
`0xf1dA173228fcf015F43f3eA15aBBB51f0d8f1123` — confirmed via multiple public sources:
- Reddit Pink Drainer fund trace: "0xf1dA173228fcf015F43f3eA15aBBB51f0d8f1123 - eXch ... sent to deposit
  addresses (eXch)"
- DefimonAlerts: "Your funding source: eXch hot wallet 0xf1dA173228fcf015F43f3eA15aBBB51f0d8f1123
  (German BKA seized eXch April 30, 2025)"
- fable/nta.sy "Investigating Hackers', Exploiters' Favorite Instant Crypto Exchange" (Oct 2024) — eXch's
  Ethereum hot wallet, used by Pink/Monkey/Inferno drainers, Lykke/Terra exploiter.

### 2. Enumerate the seed's outgoing ETH transfers in the window
Blockscout v2 `/api/v2/addresses/0xe8bde816.../transactions` (paginated via `next_page_params`): 249 txs in
window, of which **51 outgoing ETH** (from=seed, value>0) to **50 unique destinations**.

### 3. Identify eXch deposit addresses by the hot-wallet forward
For every one of the 50 destinations, fetched its full txlist and checked for an outgoing transfer to the
eXch hot wallet. **Deposit-address signature**: one-time address that receives from the seed and forwards
(minus gas) to `0xf1da1732` within ~20–90 min. Exactly **12** destinations match.

Each verified seed→deposit tx and its deposit→hot-wallet forward tx (amounts differ by gas only):
- 0xe973d58f (250 ETH, 08-30), 0xc29c7533 (210, 09-05), 0x997ff2e6 (690, 09-06), 0x1bfc76ff (750, 09-06),
  0x6d3c1d0d (50, 09-07), 0x09171fed (784, 09-08), 0x693ee0b5 (1000, 09-09), 0x507239f8 (347, 09-09),
  0x8f50d582 (1008, 09-09), 0x5cd121e1 (850, 09-09), 0x7dc05c10 (277, 09-10), 0xdc2bfe07 (1900, 09-10)

### 4. Exclude the non-eXch clusters ("secondary relay")
The other 38 destinations do NOT forward to `0xf1da1732`:
- ~30 small Aug-28 deposits (0.1–10 ETH) → `0xa7d6b757` (a relay hub, 649 outgoing spread across many EOAs)
- `0x6ef70281` (12215 ETH, Sep 4) → 27 recipients (0x98b0811E etc.) — none touch the eXch hot wallet
- `0x38862070`, `0xa00bd072`, `0x83b3eb18`→0xF40D997D, `0x1041ee03` (held until 2026) — none eXch
Also verified: no direct seed→hot-wallet txs, and no destination whose forward target is an eXch address
(checked hot wallet 0xf1da1732 + eXch DEX-balancing wallet 0x2ab34e15...).

### 5. Compute the flag
Count seed→eXch-deposit txs = 12; TOTAL_WEI = Σ values = 8116000000000000000000; first/last by timestamp.

## Data sources
- Blockscout v2 (eth.blockscout.com) — keyless txlist + pagination
- Public research: Reddit Pink Drainer trace, DefimonAlerts, fable/nta.sy eXch investigation (Oct 2024)

## Gotchas
- Recognize exchange deposit addresses by the **forward to the hot wallet**, not by amount size/freshness.
- The seed's "secondary relay" clusters (0xa7d6b757, 0x6ef70281) are NOT eXch — their downstream never
  touches the hot wallet. Verify each destination individually.
