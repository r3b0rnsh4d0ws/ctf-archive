# SCAN2026 — Challenge #5 Flag 3: Radiant Capital OPERATOR wallet

**Category:** Web3 / Multi-chain (Arbitrum, BSC, Base, Ethereum)
**Points:** 75
**Flag:** `flag{0x0629b1048298ae9deff0f4100a31967fb3f98962}`

## Challenge
Identify the operator wallet (EOA) responsible for deploying, funding, and testing the Radiant
Capital (Oct 16 2024) attack infrastructure. Supporting evidence: one test transaction it executed
before the attack (before Oct 16).

## Answer
- **OPERATOR_EOA:** `0x0629b1048298ae9deff0f4100a31967fb3f98962` (lowercase)
- **Test transaction evidence:**
  - BSC: `0x28fb8778c3c1131026b4ee3b8634106a5c1aeaaf57273cc4515c59e65dfa7eb5`
    (2024-10-02, operator → backdoor `0x57ba8957`, selector `0xfebb4f76`; **this test created the
    drainer contract `0xf0c0a1a1a19886791c2dd6af71307496b1e16aa232`** — confirmed via receipt)
  - ARB: `0x273d6b3d72d519bbc9fc9e927f8238fb52e0aae07f414ddc4b4cb22b1dbeec97` (Oct 2, `0xfebb4f76` test)
  - ARB: `0xab34055320676b35d4c6c5936dabc4101b45eda0d66b94ee02f10a96e8a1dd45` (Oct 10, `multicall` test)

## Method

### 1. Reconstructed the operator's full pre-attack footprint on 4 chains
The operator `0x0629b10482` (BscScan/Etherscan label: "Radiant Capital Exploiter") was the EOA that:
1. **DEPLOYED** the backdoor `0x57ba8957` on all 4 chains on Oct 2 (nonce 3 everywhere):
   - ARB `0x149bd3b684cf63de`, BSC `0x65419cd822bb616f`, BASE `0x45c6fc51de2fca18`, ETH `0xa0f9d89035914349`
   - plus auxiliary contracts `0x3c2bc83dcd` (BASE/ETH), `0x921b00fa` (ARB)
2. **TESTED** the backdoor before the attack — `0xfebb4f76` (createSweeper/setTargets) on all 4 chains on
   Oct 2; on BSC this deployed the drainer `0xf0c0a1a1`. More tests: Oct 10 `multicall` (ARB), Oct 14
   `multicall` on `0xbc20e84d80a6`.
3. **FUNDED** the attack infrastructure — sent small test amounts to the sweep destination
   `0x911215cf312a64c128817af3c24b9fdf66b7ac95` (labeled "Radiant Capital Exploiter 2") on all 4 chains:
   0.03 ETH (ARB), 0.03 ETH (BASE), 0.07 ETH (ETH), 0.2 BNB (BSC) — all Oct 2, all from `0x0629b10482`.

### 2. Ruled out the "different funder wallet" hypothesis
The challenge brief suggested the operator might be a separate wallet that *funded the deployer*. Traced
every funding path of `0x0629b10482`:
- **BSC:** funded by `0xe2d60cfe` (1.084 BNB, Sep 27) — an exchange-style hot wallet (nonce ~488K by 2026),
  not an attacker wallet.
- **ARB:** funded via Stargate bridge pool `0xA45B5130` (0.95 ETH, Sep 27), initiated by one-shot relayer
  `0x061aee1ac98f` (funded by `0xB38e8c17e3`).
- **BASE/ETH:** funded via Across bridge fills (executors `0x09aea4b224`, `0x5c7bcd6e7d`).
All funding dead-ends at bridges / exchange hot wallets → **no separate operator hub exists**. The deployer
is the operator (it deployed, it tested, it funded the destination).

### 3. Cross-checked other candidate addresses
- `0x911215cf` = sweep destination (received test funding, did swaps post-attack) — not a tester.
- `0x579145d6` = admin constant embedded in drainer code (no transactions).
- `0x5eb63694` / `0xD899F3d8ff` = deployed/tested `0xbc20e84d80a6` on ARB (auxiliary), but all main-chain
  test calls on the backdoor are from `0x0629b10482`.

## Data sources
- Blockscout v2 (arbitrum/blockscout.com, base.blockscout.com, eth.blockscout.com) — tx lists, internal txs
- BscScan `/txs?a=...&p=...` (server-rendered table) + BSC RPC `eth_getTransactionByHash/Receipt`
- QuillAudits Radiant post-mortem (attacker address list; drainer admin; 0xfebb4f76 creates 0xf0c0a1a1)
- BscScan/Etherscan address labels ("Radiant Capital Exploiter" / "Exploiter 2")

## Gotchas
- BscScan `/address/{a}` pagination is JS-driven; use `/txs?a={a}&p={n}` for deep history.
- BSC dataseeds are pruned for old blocks (missing trie node) — use explorer HTML or latest-state RPC.
- The "who funded the deployer?" rabbit hole leads to relayers/exchanges — that is the intended red herring.
