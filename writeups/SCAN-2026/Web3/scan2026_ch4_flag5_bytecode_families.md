# SCAN2026 — Challenge #4 Flag 5 (BSC, 175pts) — Distinct bytecode families after metadata strip

## Status: SOLVED

## Flag
`flag{1}`

## Answer
FAMILY_COUNT = 1. The deployer `0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46` deployed 16 contracts
(nonces 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,39 from Flag 4) whose runtime bytecode is
**byte-identical** (1191 B each). After stripping the 53-byte Solidity CBOR metadata, all 16 reduce
to the same 1138-byte code → **1 distinct bytecode family**.

## Method
1. Addresses: `keccak256(rlp([deployer, nonce]))[12:]` (Flag 4 list, nonce 8 = seed contract cross-check).
2. `eth_getCode(addr, 0x68c0576)` at canonical cutoff 109839734 via archive RPC
   `https://bsc-mainnet.public.blastapi.io`.
3. All 16 codes identical — verified by (a) keccak hash, (b) exact byte set (1 distinct raw code),
   (c) match against `c4_bytecode.hex` (Flag 3 artifact, keccak `0x0744dc30...`).
4. Strip Solidity CBOR metadata from LAST marker to end:
   - Actual format = **IPFS**: `a2 64 69706673 58 22 <34B multihash> 64 736f6c63 43 <3B version> 00 33`
     marker `0xa264697066735822`, solc **0.8.21** (bytes `00 08 15`).
   - Prompt-described format = bzzr0 `0xa165627a7a72305820 ... 0029` is the OLD format; NOT present here.
   - Strip both: rfind each marker, take last; 53 bytes removed.
5. Stripped code: 1138 B, keccak `0x56c1ac23688dca8391bdea7afcce2d9380b99221270ef6fca929f80515bbac57` for all 16 → 1 family.

## Gotchas
- **Archive RPC only**: blastapi serves historical `eth_getCode` at 0x68c0576; ankr `rpc.ankr.com/bsc`
  and `bsc-rpc.publicnode.com` return `0x` (empty) for block-tagged getCode — NOT full archive.
- **Metadata format trap**: the prompt's marker `a165627a7a72305820` (bzzr0) does NOT appear in this
  bytecode; solc >=0.6 defaults to IPFS metadata (`a264697066735822`). Always test both + decode the
  tail to confirm. Rule: strip from the LAST occurrence of the metadata CBOR header to EOF.
- Answer invariant here (all raw identical → all stripped identical), but the strip step matters in
  general: two contracts compiled from the same source at different times differ only in the metadata
  hash → 1 family only AFTER stripping.
- BscScan V1 proxy API is deprecated (NOTOK "switch to Etherscan API V2"); V2 needs a paid plan for
  BSC. Use archive RPC + existing verified artifacts instead.

## Files
- Solver: `flag5_distinct_families.py` (challenge folder)
- Research: `D:\CTF\data\research\web3\scan2026_bsc_arb.md`
