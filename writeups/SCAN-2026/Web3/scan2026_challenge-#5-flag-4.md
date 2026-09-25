# SCAN 2026 — Challenge #5 Flag 4 (125 pts) — Radiant Capital Admin Takeover

## Flag
```
flag{transferOwnership|0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5}
```

## Challenge
- **Category**: Web3 / Blockchain forensics (READ-ONLY)
- **Network**: Arbitrum One
- **Takeover tx**: `0x7856552db409fe51e17339ab1e0e1ce9c85d68bf0f4de4c110fc4e372ea02fb1`
- **Task**: Identify the function that transferred administrative control of Radiant Capital and the new owner.

## Background
Radiant Capital exploited Oct 16, 2024. Malware on developer devices altered transactions
shown in the Safe UI; the developers unknowingly signed a transaction that handed the
protocol's admin (ownership of the PoolAddressesProvider) to the attacker. The attacker
then swapped the LendingPool implementation to a malicious one and drained 12 pools.

## Method (read-only, no txns)

### 1. Fetch tx
`eth_getTransactionByHash` on `https://arb1.arbitrum.io/rpc`:
- from: `0x0629b1048298ae9deff0f4100a31967fb3f98962` (Arbiscan label: "Radiant Capital Exploiter 1")
- to:   `0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5` (attacker's pre-deployed multicall contract, deployed Oct 2, 2024)
- block: 264477049, Oct-16-2024 05:09 PM +UTC

### 2. Decode outer calldata
- selector `0x63fb0b96` = `multicall(address[] contracts, bytes[] data)` (4byte.directory)
- 3 recipients, 3 data blobs.

### 3. Decode inner calls
**data[0] → `0x111ceeee040739fd91d29c34c33e6b3e112f2177`** (Gnosis Safe, 171-byte proxy, emits `SafeMultiSigTransaction`):
- selector `0x6a761202` = `execTransaction(address,uint256,bytes,uint8,uint256,uint256,uint256,address,address,bytes)` (Gnosis Safe)
- to = `0x091d52cace1edc5527c99cdcfa6937c1635330e4` (Radiant **PoolAddressesProvider**)
- data = `0xf2fde38b` = **`transferOwnership(address)`** → newOwner = **`0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5`**
- signatures = 195 bytes = 3 × 65-byte ECDSA signatures (Safe owners signed the malware-modified tx)

**data[1] → `0x091d52...` (PoolAddressesProvider)**:
- selector `0x5aef021f` = `setLendingPoolImpl(address)` → `0xF0C0a1A19886791c2DD6aF71307496b1E16aA232` (attacker's malicious LendingPool impl)

**data[2] → `0xf4b1486dd74d07706052a33d31d7c0aafd0659e1`** (Radiant LendingPool proxy, EIP-1967 impl slot → `0x3d4c56cd...`):
- selector `0x191ba4ed` = `go(address[],address)` (openchain signature DB) — drains 12 tokens to `0x0629...`

### 4. Receipt logs confirm
- `SafeMultiSigTransaction` (Safe `0x111ceeee...`)
- **`OwnershipTransferred(previousOwner=0x111CEEee..., newOwner=0x57ba8957ed2ff2e7AE38F4935451E81Ce1eEFbf5)`** on `0x091d52...`
- `ExecutionSuccess` (Safe)
- `Upgraded(0xF0C0a1A1...)` on LendingPool proxy
- `LendingPoolUpdated(0xF0C0a1A1...)` on PoolAddressesProvider
- 12 ERC-20 `Transfer` events → exploiter

### 5. Cross-check
`eth_call owner()` on `0x091d52...` at latest → `0x00000000000000000000000057ba8957ed2ff2e7ae38f4935451e81ce1eefbf5` ✔

## Answer
- **FUNCTION_NAME** = `transferOwnership`
- **NEW_OWNER** = `0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5`
- Flag: `flag{transferOwnership|0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5}`

## Files kept
- `decode_tx.py` — local ABI decoder for the tx
- `tx_input.hex`, `tx.json` — raw tx data (kept for reproducibility)
