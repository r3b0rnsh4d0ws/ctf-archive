# SCAN2026 — Challenge #9: DEX admin-fee skim — "one transaction to stop the bleeding" (600 pts)

## Flag
```
flag{0x704b6c020000000000000000000000003fb80ed7451795b02a18ea6a7e31f83acbe1f38c}
```

## The fix transaction
| field | value |
|-------|-------|
| from | `0x3fb80eD7451795b02A18EA6A7e31F83acbE1F38C` (Nino/owner) |
| to   | `0x248E97Dac4796C78e2531b95f7Aaab83b6Bc2379` (DEX) |
| value | 0 |
| calldata | `0x704b6c02` + `0000000000000000000000003fb80ed7451795b02a18ea6a7e31f83acbe1f38c` |

`0x704b6c02` = `setAdmin(address)`. The owner sets the DEX admin to themselves, closing the
"anyone is admin" backdoor that lets any caller run `withdrawAdminFees`.

## Where the contracts actually live
The three challenge addresses (`0x248E97...`, `0xcabDd7...`, `0x571FD7...`) have **zero nonce and
zero code on Ethereum mainnet**. Scanning ~90 EVM chains found code only on **Base Sepolia**
(testnet). All SCAN2026 web3 challenges are deployed there.

## Root cause — unset admin opens `_isAdmin` to everyone
Verified DEX contract (sepolia.basescan.org, "Contract Name: Dex", solc 0.8.26, optimizer 200).
Constructor args decode to `_admin = 0x0000000000000000000000000000000000000000`.

Bytecode at `0x0bd3` decompiles to:
```solidity
function _isAdmin(address who) internal view returns (bool) {
    if (admin == address(0)) return true;   // backdoor
    return who == admin;
}
```
On-chain `admin()` (slot 4) = `0x0...0`. Therefore `_isAdmin` returns true for **any** caller.
Combined with `withdrawAdminFees(address to)` (selector `0xb0630715`, onlyAdmin) and
`setAdmin(address)` (selector `0x704b6c02`, onlyAdmin), anyone could:
1. call `withdrawAdminFees(<their wallet>)` → drain `adminFees0/adminFees1` (slots 5/6), or
2. call `setAdmin(<their address>)` → take over the DEX.

A skimmer `0xE31b9fBB...` is visible in the DEX tx history calling "Withdraw Admin F..." — that's
the "someone skimming off the top".

## Verification (all via eth_call on Base Sepolia)
- `admin()` → `0x0...0` (admin never set) ✓
- `withdrawAdminFees(skimmer)` **from the skimmer** → success (the bleed) ✓
- `setAdmin(owner)` **from the owner** → success (the fix) ✓
- after the fix, `_isAdmin(owner)` is true only for the owner → skimmer's next withdraw reverts.

## Key lesson
The "one transaction that fixes it" challenge pattern: a modifier/guard built on an unset
state variable (admin/owner = zero address) that degrades to "allow all". Fix = write the
authority value once (`setAdmin(owner)`). Build calldata as
`selector + abi.encode(address)` (32-byte right-padded).
