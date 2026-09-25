# SCAN2026 — Challenge #6 Flag 4 (225 pts): Tornado Cash cross-chain consolidation on TRON

**Status:** SOLVED

**Flag:** `flag{TJJkwYS4EMYL5T34eDRqyGzbs18bwbdEHC}`

## Question
The funds in the 13 Tornado Cash withdrawing addresses consolidate on another network. Trace the fund
movements forward until you find the consolidation point; submit that address (case-sensitive, TRON base58).

## Answer
**TJJkwYS4EMYL5T34eDRqyGzbs18bwbdEHC** — the single USDT-TRC20 address where all 13 withdrawal streams
merge (total 488,173.75 USDT ≈ 130 ETH at ~$3,755/ETH in June 2024).

## End-to-end trace (all verified on-chain)

### Ethereum leg: WDs → KyberSwap swapBridgeToV2
1. All 13 WD EOAs call the KyberSwap aggregator proxy `0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f`
   (40 txs, selector `0x3d21e25a`). Each WD splits its ~9.9 ETH into 3–5 chunks (5.0 + 4.9 + small 0.01–0.05).
2. Full ABI (hand-parsed from `raw_input`):
   `swapBridgeToV2((address,address,address,uint256,uint256,uint256,uint256,uint256,bytes,bytes,bytes))`
   = (srcToken=ETH, dstToken=USDT 0xdac17f95…, srcReceiver=<per-WD EOA>, dstReceiver=0x0…3, amount,
   minReturnAmount, guaranteedAmount=nonce, permit, data, **hint**).
3. The **hint** (128 bytes, 3rd dynamic field) contains a **plaintext TRON base58 address** — the
   USDT-TRC20 destination for the SwftSwap (`0x92e929d8…`) cross-chain leg. Every swap tx of a given WD
   carries the same TRON address → 13 unique TRON addresses total.

### TRON leg: SwftSwap delivery → consolidation
4. SwftSwap TRON operator wallet `TEorZTZ5MHx8SrvsYs1R3Ds5WvY1pVoMSA` (762k txs, still active 2026) pays
   ~37K USDT-TRC20 to each of the 13 hint addresses (2–3 deposits each, matching the ETH chunks + dust).
5. **Consolidation:** each of the 13 TRON addresses forwards its ENTIRE USDT balance in ONE transfer to
   `TJJkwYS4EMYL5T34eDRqyGzbs18bwbdEHC` within minutes (ts 1717355574 → 1717498035 = 2024-06-02 22:32 →
   2024-06-04 13:27 UTC). Sum = 488,173.75 USDT.
6. TJJkwYS was **created 2024-06-02 07:03 UTC** (pre-created consolidation wallet, 97 txs) and later
   disperses to ~7 downstream addresses (TJb9bos… ×6, TU5bo3…, TRRbZms…, TThiSnR…, TDA4REC…, TVcb3qZ…) —
   exchange/OTC onward movement, not the answer.

### 13 → 1 transfer table (TRON source → TJJkwYS, USDT)
| WD (ETH) | TRON source | amt | tx |
|---|---|---|---|
| 0x96dc12a1 | TWAZsqYC8TVnGHaKTzwuhErHwFeyeHheCU | 37,293.37 | bb95dea4… |
| 0x54212c93 | TCLKPykGXJk81QWxnHxSDRgepUmtLySxS3 | 37,341.89 | f952aecc… |
| 0xab2b6f1f | TTYeTzmjqymnuFeG7HEHNxcUWAvr9Q7zJf | 37,923.08 | beec16f7… |
| 0x8ba0aba8 | TCeVs9dfG4bwb7kB2RXUUUezcHAyyabJs4 | 37,933.44 | 6a8d6d3c… |
| 0xdc804997 | TBJx4EcGHiB4duxS7KbwzqYGqgG3F13RRK | 37,764.86 | 278aaabb… |
| 0xaeca1d64 | TE2E1Drw6zU7o3mKf2QN7pnTuEqbv39xqz | 37,752.95 | cfc3dc79… |
| 0xe315b8d4 | TPbyrQ3aVXu5sBcw3VAMVQqM9JNvnZT2Sg | 37,910.42 | 3a0bd869… |
| 0xdccf86d4 | TFJSA7wLbhahszADZqbAY4NvcUq178jfq7 | 37,927.96 | 4bdda003… |
| 0x01900453 | TRuwuMF8iBuPq6WSHvvkkdUZgHiKhp11mH | 37,412.70 | 039bff0a… |
| 0x371e628d | TFc4XyFEWaaK3zHmzD6fsVM7i4Uzcn3zFb | 37,421.01 | d8e9329e… |
| 0x42242156 | TS9oYkjy6we9QCnzxyzpRo2D94mTuxb4mP | 37,142.11 | bccf1bf4… |
| 0xbe5e23e0 | TAr7ewdyTkJVNT4b5kqmPATmeMmDyKgwqg | 37,121.80 | 5206bb86… |
| 0x144cf3db | TGkje2cBdks76jP73Afd3efmb6sLtCRJhC | 37,228.16 | 8c8db43b… |
| **TOTAL** | | **488,173.75** | |

## Tools & data sources
- Blockscout v2 `eth.blockscout.com/api/v2` — WD txlists (`/addresses/{a}/transactions`) + tx raw_input
  (`/transactions/{hash}`).
- Manual ABI parsing of `swapBridgeToV2` struct (unverified proxy → decoded_input useless; raw_input is truth).
- TronScan public API `apilist.tronscanapi.com/api/token_trc20/transfers?limit=50&start=N&sort=-timestamp&count=true&relatedAddress=…&contract_address=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` (USDT-TRC20; limit>50 → HTTP 400, paginate 50s).
- TRON base58 validation: decode → 25 bytes, version byte 0x41, 4-byte double-SHA256 checksum.

## Files
- `C:\Users\balu\ctf-shared\scan2026\c6f4_*.py` + `c6f4_*.json` (fetch/parse/verify scripts + caches)
- `D:\CTF\ctfs\0_scan2026\challenges\challenge-#6-flag-4\progress.md`

## Key lessons
- KyberSwap `swapBridgeToV2`'s `hint` field carries the plaintext cross-chain destination address — decode
  dynamic struct fields yourself instead of trusting explorer decode on unverified proxies.
- Cross-chain consolidation point = the ONE address that every delivery address empties into in a single
  transfer. Downstream dispersal = not the answer.
- Flag is case-sensitive TRON base58; prior writeups may carry a transposed address
  (`...FeyeHeCeU` vs on-chain `...FeyeHheCU`) — always round-trip against TronScan.
