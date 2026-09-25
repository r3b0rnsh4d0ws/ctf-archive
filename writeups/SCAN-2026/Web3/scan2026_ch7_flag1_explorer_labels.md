# SCAN2026 — Challenge #7 Flag 1: Lazarus stablecoin freeze checks (Ronin Exploiter)

**Category:** Web3 / OSINT (Ethereum mainnet) · **Pts:** 125 · **Status:** SOLVED
**Flag:** `flag{Ronin Bridge Exploiter|addBlackList|true}`

## Task (from metadata.yml)
Lazarus group (APT38) laundering case. For the Ronin Exploiter address
`0x098B716B8Aaf21512996dC57EB0615e2383E2f96`:
1. Etherscan public name tag
2. Exact USDT function that adds an address to the blacklist
3. USDC `isBlacklisted()` result for that address
Submission: `flag{ETHERSCAN_LABEL|USDT_FUNCTION|USDC_BLACKLISTED}` (label may contain spaces).

## Part (a) — Etherscan label: `Ronin Bridge Exploiter`
`etherscan.io` is Cloudflare-protected (403 "Just a moment..." even via reader). **Wayback Machine**
has 278 captures of this address page. The capture from 2025-01-10 shows:
- Banner: *"This address is reported to be involved in a hack targeting the Ronin bridge."*
- Public name tag: **Ronin Bridge Exploiter** with sub-tags **Exploit / OFAC-Sanctioned / Blocked**
- Funded by Binance (tx 0xe0669b…); on 2022-05-03/04 sent 12,595.3 ETH → OFAC Blocked 0x087…243 and
  23,528.8 ETH → OFAC Blocked 0x3e3…5e9 — consistent with the March 2022 Ronin bridge hack laundering.

## Part (b) — USDT freeze function: `addBlackList`
USDT = `0xdAC17F958D2ee523a2206206994597C13D831ec7` (TetherToken, verified).
- The challenge metadata hint said selector `0x01e1d74a` — this is **wrong** (not in 4byte DB; count=0).
- Correct: `keccak256("addBlackList(address)")` = **`0x0ecb93c0`** (computed with pycryptodome
  `Crypto.Hash.keccak`); 4byte.directory entry id 36770 (submitted 2018-06-24) confirms
  `addBlackList(address)` = 0x0ecb93c0.
- Exact casing verified against the verified ABI (Blockscout v2 smart-contracts endpoint): functions
  `addBlackList`, `removeBlackList`, `getBlackListStatus`, `isBlackListed`; events `AddedBlackList`,
  `RemovedBlackList`. So the freeze function is **`addBlackList`** (capital B, capital L).
- Extra on-chain proof: `eth_call` `getBlackListStatus(address)` (0x59bf1abe) on USDT for the Ronin
  address → `0x…01` = **true** — Tether already blacklisted it.

## Part (c) — USDC isBlacklisted: `true`
USDC = `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (upgradeable proxy).
`eth_call` `isBlacklisted(address)` (selector 0xfe575a87, verified by keccak) with the padded Ronin
address → `0x0000000000000000000000000000000000000000000000000000000000000001` = **true**.

## Tools / endpoints used
| Purpose | Endpoint |
|---|---|
| Etherscan page (blocked) → Wayback | `https://web.archive.org/web/20250110192405/https://etherscan.io/address/0x098B...` |
| Selector DB | `https://www.4byte.directory/api/v1/signatures/?text_signature=addBlackList(address)` |
| Verified ABI | `https://eth.blockscout.com/api/v2/smart-contracts/0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| eth_call RPC | `https://ethereum-rpc.publicnode.com` (llamarpc → HTTP 521; ankr → empty body) |
| keccak | pycryptodome `Crypto.Hash.keccak` (256-bit, Ethereum variant) |

## Gotchas / lessons
1. **Challenge hint selectors are not always correct** — always re-derive via keccak + 4byte.
   The metadata's `0x01e1d74a` for `addBlackList` is bogus; the real one is `0x0ecb93c0`.
2. **Etherscan scraping**: Cloudflare 403 even via Jina reader; Wayback Machine captures preserve the
   name-tag text perfectly and are an OSINT-legal way to read the displayed label.
3. **Upgradeable proxies**: `isBlacklisted` works on the proxy address (implementation fallback) —
   no need to resolve the implementation.
4. **Public RPC reliability**: try several; `ethereum-rpc.publicnode.com` and
   `rpc.ankr.com` worked, `eth.llamarpc.com` returned 521 during this run.

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\challenge7_flag1.py`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#7-flag-1\progress.md`

## 2026-08-03 addendum (independent re-verify)
- Etherscan direct curl with full browser UA worked this run (Cloudflare wall intermittent): name tag
  "Ronin Bridge Exploiter" found verbatim in 584KB HTML. Backup: Wayback (see notes).
- USDT ABI exact functions verified from Etherscan contract page: addBlackList/removeBlackList/
  getBlackListStatus/isBlackListed/destroyBlackFunds; addBlackList selector 0x0ecb93c0.
- USDC isBlacklisted(Ronin) = true on 3 independent RPCs (publicnode, blastapi, tenderly).
Solver: C:\Users\balu\ctf-shared\scan2026\challenge7_flag1.py (runs clean)
