# SCAN2026 — Challenge #4 Flag 4 (225pts, BSC) — Count deployer's contracts at cutoff block

## Flag
`flag{16}`

## Challenge
Given the clipboard-hijacker C2 deployer 0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46 (from Flag 1),
compute CREATE addresses for ALL nonces and check which had deployed code AS OF canonical cutoff
block 109839734 (0x68c0576) via eth_getCode with block tag. Count total contracts with code.
Answer: flag{CONTRACT_COUNT}.

## Method
1. **Nonce bound at cutoff**: `eth_getTransactionCount(deployer, 0x68c0576)` = `0x50` = 80 nonces
   used as of the cutoff block (archive RPC `https://bsc-mainnet.public.blastapi.io`).
   NOTE: BscScan "latest" tx count is 105 — that includes post-cutoff txs and would over-count.
2. **Derive CREATE addresses**: for each nonce 0..79,
   `addr = keccak256(rlp([deployer_bytes, nonce]))[12:]` (pure Python: pycryptodome keccak + custom
   minimal RLP encoder — web3/eth_utils not installed on the machine).
3. **Check code at cutoff**: `eth_getCode(addr, "0x68c0576")` for each of the 80 addresses;
   count results != `0x`. Block-tagged getCode automatically excludes:
   - contracts deployed after the cutoff (no code at that block yet),
   - selfdestructed contracts.
4. **Result**: 16 addresses have code (all 1191 bytes):
   nonces 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,39.
5. **Validation**:
   - nonce 8 → `0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468` = the known seed contract (Flag 1
     cross-check). Code fetched at cutoff is byte-identical to `c4_bytecode.hex` (2382 hex chars).
   - nonce 39 → tx `0x223f54e7...` nonce 0x27, block 0x55cfa67 (89,979,495) — before cutoff.
   - BscScan `/txs?a=<deployer>` HTML scrape: exactly 16 rows contain "Contract Creation",
     all within the scenario window (2026-03-16 onward). Independent confirmation of the count.

## Flag
`flag{16}`

## Files
- `flag4_count_contracts.py` — RPC CREATE-address enumeration + block-tagged getCode count
- `flag4_txlist_check.py` — BscScan txlist scrape cross-check (counts "Contract Creation" rows)

## Key lesson
"Count contracts at block X" = block-tagged `eth_getCode` over the block-tagged nonce range
(`eth_getTransactionCount(..., blockTag)`). Using the "latest" tx count bounds the wrong (larger)
set; only archive-RPC block-tagged reads give the cutoff picture.
