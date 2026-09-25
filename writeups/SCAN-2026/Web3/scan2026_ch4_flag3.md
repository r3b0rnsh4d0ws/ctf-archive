# SCAN2026 - Challenge #4 Flag 3: read getter at cutoff block (125pts)

**Flag:** `flag{uint256|string|kffd3.vexlatech.cc|96}`

**Seed contract:** 0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468 (BSC, unverified clipboard-C2)
**Cutoff block:** 109839734 (0x68c0576), hash 0x87313e41bdeec09e5ef167cf32ba72b7f7812c97f11c5666e3251986278c9364, ts 2026-07-13T23:59:59Z. Verified: next block 109839735 = 2026-07-14T00:00:00Z.

## Answers
| Field | Value |
|---|---|
| STANDARD_RETURN_TYPE | uint256 (ERC-20 balanceOf spec) |
| ACTUAL_RETURN_TYPE | string (Solidity string getter) |
| DECODED_DOMAIN | kffd3.vexlatech.cc |
| RAW_RETURN_BYTE_COUNT | 96 |

## Method
1. `eth_call` `0x70a08231` + 32 zero bytes (input discarded) with blockTag `0x68c0576` on BSC.
   - Public dataseeds fail for historical state ("missing trie node" / pruned / 1rpc rate-limit / ankr auth).
   - **`https://bsc-mainnet.public.blastapi.io` (archive) works.**
2. Raw return (96 bytes):
   ```
   00..0020   -> offset = 32
   00..0012   -> length = 18
   6b666664332e7665786c61746563682e6363 -> "kffd3.vexlatech.cc"
   ```
3. Cross-check `eth_getStorageAt` slot 0 @cutoff = `0x6b666664332e...6363...24` (Solidity short-string,
   last byte 0x24 = 2Ã—18). Both reads agree.
4. Bytecode: getter at PC 293 does `PUSH1 0x60 PUSH0 DUP1 SLOAD` â†’ 0x2a9 string-decode â†’ standard
   Solidity string ABI return (offset+len+data). So ACTUAL_RETURN_TYPE = string.

## Key gotcha
- The domain **rotates**: at cutoff it is `kffd3.vexlatech.cc`, at latest it is `lB.propertyfind.cc`.
  The "Flag 2" domain (`lB.propertyfind.cc`) is the CURRENT state â€” using it is the trap. Metadata says
  "current chain state is not the answer"; must evaluate at the cutoff block.
- RAW_RETURN_BYTE_COUNT = total raw bytes returned by eth_call (32+32+32 = 96), matching the example's
  "bytes32 â†’ 32" logic (full raw return length).
