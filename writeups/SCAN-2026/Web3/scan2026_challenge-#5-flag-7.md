# SCAN2026 — Challenge #5 Flag 7 — Radiant Capital laundering consolidation address (Ethereum)

**Status: SOLVED** · **Points: 200** · **Flag: `flag{0x961a19d16db31add5e257bc3d73b403ee0d3680e}`**

## Task
After the Oct 16 2024 Radiant Capital theft, the attacker consolidated assets from multiple
blockchains by swapping tokens, bridging to Ethereum, and routing through intermediary wallets.
Trace the laundering path on Ethereum from the operator wallet
(`0x0629b1048298ae9deff0f4100a31967fb3f98962`, the deployer EOA identified in Flag 3).
Submit the address that received the LUMP and then HELD it (no movements) for MONTHS before forwarding.

## Answer
`0x961a19d16db31add5e257bc3d73b403ee0d3680e`

- Received lump: **2024-10-18 01:03:11 UTC**, 706.953640874178 ETH (tx `0xfd04fc78...`, from `0x8b75e47976c3c5...`)
- Held with **zero outgoing transactions for ~10.2 months**
- Forwarded: **2025-08-25 10:47:11 UTC**, 707.053584778178 ETH (tx `0x2e2105f5...`, nonce `0x0` =
  the address's very first outgoing tx) to `0x828d4067eb67a1bf86c3bea958ee14a825f3bf69`

## The laundering chain on Ethereum
| hop | address | lump in | first out | hold |
|---|---|---|---|---|
| op | `0x0629b1048298ae9deff0f4100a31967fb3f98962` (operator) | received 1,864,777.25 MIM via LayerZero OFT bridge (`LzProxyOFTV2 0x439a5f0f5E8d14`, tx `0x18a5c886...`); swapped MIM→ETH via router `0xCf5540fFFCdC3d` (fn `0x83bd37f9`, txs `0xb42a4961cd` FAIL then `0x618b44e44c` OK, internal return 706.78 ETH) | 10-16 20:36:35 | – |
| 1 | `0x97a05becc2e7891d07f382457cd5d57fd242e4e8` | 10-16 20:36:35 (707.0543 ETH, `0x1676df6ff4`) | 10-16 23:28:59 | ~3h |
| 2 | `0x8b75e47976c3c500d0148463931717001f620887` | 10-16 23:28:59 | 10-18 01:02:23 | ~1.5d |
| 3 | **`0x961a19d16db31add5e257bc3d73b403ee0d3680e`** | **10-18 01:03:11 (706.9536 ETH)** | **2025-08-25 10:47:11 (nonce 0)** | **~10.2 months** |
| 4 | `0x828d4067eb67a1bf86c3bea958ee14a825f3bf69` | 08-25 2025 | 08-27 2025 | split onward (→ `0xfba1af29...`, → 1inch Router `0x1111111254...`) |

## Method (read-only)
1. Operator EOA from Flag 3. Fetched full Ethereum tx list via Blockscout v2
   (`https://eth.blockscout.com/api/v2/addresses/<addr>/transactions`).
   Operator has only 18 ETH txs total — small enough to enumerate fully.
2. Identified the 4 outgoing txs on 10-16: `0x095ea7b3` approve on MIM (`0x99D8a9C45b2e`),
   two `0x83bd37f9` router calls (first reverted, second succeeded), and one plain-value ETH lump
   `0x1676df6ff4` → `0x97a05becc2e7...` of **707,054,326,361,894,848,263 wei**.
3. Traced the lump hop-by-hop by querying each recipient's tx list and picking big native-value
   outgoing txs. Hops 1-2 moved within hours/days; hop 3 (0x961a...) had NO outgoing until
   2025-08-25.
4. Verified candidate:
   - EOA (`eth_getCode` == `0x`), not a contract;
   - inbound receipt `status 0x1`;
   - outbound forwarding tx nonce `0x0` and `eth_getTransactionCount` == 1 → never sent before;
   - no token transfers / internal movements out during the hold (Blockscout token-transfers +
     internal-transactions lists).
5. Cross-checked inbound lump and outbound forwarding via independent public RPC
   (`ethereum-rpc.publicnode.com`, browser UA required).

## Gotchas / red herrings
- The operator also received 3 txs of a **fake "ЕТН" token** (Cyrillic "Е", contract
  `0x0b87745565eF162c017Bc57dcC2154518c0cDFff`, total supply 1e36, worth $0) whose transfer value
  is byte-identical to the real ETH lump (707054326361894848263). Must inspect the token address,
  not just the wei value.
- Blockscout v2 `items_count` max is 50 (422 otherwise).
- Most public Ethereum RPCs 403 without a browser User-Agent header.

## Files
- Solver: `flag7_solve.py` (in challenge dir + `C:\Users\balu\ctf-shared\scan2026\`)
- Research notes: `D:\CTF\data\research\web3\scan2026_bsc_arb.md`
