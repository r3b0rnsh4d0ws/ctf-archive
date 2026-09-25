# SCAN2026 — Challenge #5 Flag 2: Multi-chain same-address Radiant backdoor (75 pts)

## Flag
`flag{4|14}`

## Answers
- **CHAINS** = `4` — Arbitrum, BSC, Base, Ethereum (identical 11148-byte code at
  `0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5`; every other tested chain empty).
- **t_deploy** = 1727831557 = **2024-10-02T01:12:37Z** (Arbitrum block 0xf76d3d1 — earliest of the 4).
- **t_takeover** = 1729098558 = **2024-10-16T17:09:18Z** (Arbitrum block 0xfc39979,
  tx `0x7856552db409fe51e17339ab1e0e1ce9c85d68bf0f4de4c110fc4e372ea02fb1`).
- **DAYS** = `14` = floor((1729098558 − 1727831557)/86400) = floor(1267001/86400) = floor(14.6648).

## Deployment matrix (same EOA 0x0629b1048298ae9deff0f4100a31967fb3f98962, nonce 3 on all → same address)
| Chain | Creation tx | Block | Timestamp (UTC) |
|---|---|---|---|
| Arbitrum | 0x149bd3b684cf63decffbdd1865a20fddf131fb59469d093b2b6d9aa57a0ce4c2 | 0xf76d3d1 | 2024-10-02T01:12:37Z |
| BSC | 0x65419cd822bb616f2d9dacbcfacf81714761f9815cc26b9451cd70f0348232fa | 0x28c7410 | 2024-10-02T08:22:46Z |
| Base | 0x45c6fc51de2fca18d9b102e59eb6a12ada42f0ddb078216138d857cd83033981 | — | 2024-10-02T08:34:51Z |
| Ethereum | 0xa0f9d89035914349198a56ddddb0c3d93e092e7fb37ecaf9d26cba741708aa89 | — | 2024-10-02T08:41:35Z |

## Method
1. **Chain sweep:** `eth_getCode(addr,"latest")` on 30+ EVM chains. Code (len 11148) found ONLY on
   Arbitrum, BSC, Base, Ethereum. Fantom verified EMPTY on two independent endpoints
   (rpcapi.fantom.network, fantom.drpc.org). Optimism/Polygon/Avalanche/etc. all empty.
2. **Creation txs per chain:**
   - Arbitrum/BSC: RPC `eth_getTransactionReceipt` → `contractAddress == 0x57ba...`; nonce 0x3 both.
   - Base/Ethereum: Blockscout V2 API (no key): `/api/v2/addresses/{addr}` →
     `creation_transaction_hash` + `creation_status: success`; then `/api/v2/transactions/{hash}` →
     timestamp. All creators = the same attacker EOA.
   - The identical-address trick = CREATE derivation `keccak(rlp([from,nonce]))[12:]` is
     chain-independent: same EOA + same nonce (3) + same init code ⇒ same address on every EVM chain.
3. **Takeover tx** `0x7856552d...` is ON ARBITRUM: attacker EOA → malicious contract,
   selector `0x63fb0b96` (the backdoor's own `setTargets`/sweep function, from its dispatcher),
   block 0xfc39979, ts 1729098558 = 2024-10-16T17:09:18Z — the S4 takeover of the Oct 16 Radiant attack.
4. **DAYS** computed from UTC block timestamps.

## Notes / gotchas
- Public RPC landmines: 1rpc.io rate limit; rpc.ftm.tools & polygon-rpc.com "API key disabled"; 
  eth.llamarpc.com returned HTML for this call; omniatech/blockpi 521. Redundancy list that works:
  bsc-dataseed1/2, ethereum-rpc.publicnode.com, polygon-bor-rpc.publicnode.com, fantom.drpc.org,
  mainnet.base.org, arb1.arbitrum.io/rpc.
- Blockscout V2 requires lowercase addresses and returns the creation fields only for contracts.
- Public writeups focus on the theft chains (Arbitrum + BSC) but the on-chain truth is 4 chains — trust RPC.

## Files
- `sweep_chains.py`, `timeline.py`, `creation_txs.py`, `bsc_creation.py`
- `D:\CTF\data\research\web3\scan2026_bsc_arb.md` — technique notes
