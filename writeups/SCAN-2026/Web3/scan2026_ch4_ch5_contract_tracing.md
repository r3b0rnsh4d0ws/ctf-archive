# SCAN2026 — Challenge #4 (BSC) + #5 (Arbitrum): Blockchain contract-tracing

## Challenge #4 — Clipboard C2 seed contract (BSC, 75 pts)
Seed: `0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468` (BSC Mainnet, unverified bytecode).

**Question:** Deployer address, deployment tx hash, CREATE nonce.
**Answer:**
```
flag{0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46|0x538c45776a80c71c255920854230935ab55038d4d11746999ac2fd5b630f92d2|8}
```
- Deployer: `0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46`
- Create tx: `0x538c45776a80c71c255920854230935ab55038d4d11746999ac2fd5b630f92d2`
- Nonce: `8`

**Method:**
1. BscScan V1 `getcontractcreation` API is deprecated (NOTOK); V2 (`api.etherscan.io/v2/api`) requires paid plan for chain 56 → scrape HTML.
2. `https://bscscan.com/address/0x7cc3...` (browser UA) → "Contract Creator" block: creator link + create-tx link (`/tx/0x538c...`).
3. Cross-check: creator address `0x3a35b409...` inlined in runtime bytecode as immutable `owner` constant.
4. BSC public RPC `eth_getTransactionByHash` → `to: null`, `nonce: 0x8` (CREATE nonce = account nonce used).
5. `eth_getTransactionReceipt` → `contractAddress == 0x7cc3cfc1...` (creation confirmed).

## Challenge #5 — Radiant Capital backdoor (Arbitrum, 75 pts)
Deploy tx: `0x149bd3b684cf63decffbdd1865a20fddf131fb59469d093b2b6d9aa57a0ce4c2`

**Question:** Contract created by this tx.
**Answer:**
```
flag{0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5}
```
- Created contract: `0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5` (Radiant Capital Oct-2024 backdoor, deployed by `0x0629b1048298ae9deff0f4100a31967fb3f98962`, nonce 3).

**Method:**
1. `eth_getTransactionByHash` (arb1.arbitrum.io/rpc) → `to: null` = creation.
2. `eth_getTransactionReceipt` → `contractAddress: 0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5` (authoritative).
3. Fallback if no receipt: `keccak256(rlp([from, nonce]))[12:]`.

## Key lessons
- `eth_getTransactionReceipt.contractAddress` answers "what did this tx create" instantly.
- Contract Creator block on explorer pages answers "who deployed this / at which tx"; nonce = that tx's `nonce` field via RPC.
- Immutable variables (Solidity `immutable`) are inlined into bytecode — grep bytecode to confirm owner/deployer.
- PowerShell 5.1 mangles `"` escapes in curl -d JSON → write payload to file, use `--data "@file.json"`.
