# SCAN2026 — Challenge #4 Flag 2: Clipboard C2 runtime bytecode disassembly (150 pts, BSC)

## Flag
`flag{70a08231|47064d6a|00|caller_check}`

## Answers
- **GETTER_SELECTOR** = `70a08231` — ERC-20 `balanceOf(address)` disguise. Dispatcher routes it to the
  string getter which **discards the input** and returns the C2 domain string from storage slot 0.
- **SETTER_SELECTOR** = `47064d6a` — a separate function (NOT the balanceOf disguise) that writes the
  domain string to slot 0.
- **STORAGE_SLOT** = `00` — the domain string lives at slot 0 (Solidity `string` layout: short string
  packed in-slot with len<<1, low bit 0; getter/setter routines confirm slot 0).
- **ACCESS_CONTROL** = `caller_check` — `CALLER` (msg.sender) must equal owner
  `0x3a35b409af86e79e8945d6a7ffb1dc59b8dbdf46` (the deployer), else `0x08c379a0` revert `"Only owner"`.
  No `ORIGIN` opcode anywhere in the 2382-byte runtime.

## Contract
- Seed: `0x7cc3cfc1ac007b8c6566fd2c7419b15a75473468` (BSC Mainnet, chain 56), unverified bytecode.
- Canonical block 109839734 (0x68c0576), 2026-07-13T23:59:59Z cutoff.

## Method
1. **Bytecode fetch:** `eth_getCode(seed, 0x68c0576)` on public BSC dataseeds returns
   `{"error":{"code":-32000,"message":"missing trie node"}}` — state is pruned at the canonical block.
   Runtime code is immutable (contract not selfdestructed), so `eth_getCode(...,"latest")` returns the
   identical 2382 bytes. (Verify: no SELFDESTRUCT opcode in the disassembly.)
2. **Disassembly:** `pip install pyevmasm` is BROKEN on py3.10 (`disassemble_all` raises
   `TypeError: can only concatenate str (not int) to str`). Wrote a 30-line opcode-table disassembler
   (dict 0x00..0xff, PUSHn operand emission) — clean output.
3. **Dispatcher (PC 0-43):** `CALLDATASIZE PUSH1 04 LT` → revert if calldata < 4 bytes; then
   `CALLDATALOAD PUSH1 e0 SHR DUP1 PUSH4 47064d6a EQ PUSH2 002c JUMPI` (setter branch) and
   `DUP1 PUSH4 70a08231 EQ PUSH2 0041 JUMPI` (getter branch); fall-through revert.
4. **Getter (PC 0x41=65 → 0x125=293):** non-payable check (`CALLVALUE ISZERO`), ABI-decodes an
   `address` arg (routine 0x222 — decoded but unused!), then `PUSH1 0x60 PUSH0 DUP1 SLOAD` reads
   **slot 0** and runs the Solidity bytes-to-string routine (0x2a9) → returns the domain string.
5. **Setter (PC 0x2c=44 → 0x76=118):** ABI-decodes a dynamic `string` arg (routine 0x1b6), then:
   - PC 119: `CALLER` → `PUSH1 01 PUSH1 01 PUSH1 a0 SHL SUB` (address mask) → `PUSH20 owner`
     `AND EQ JUMPI 0xdf`; else revert `Error(string)` "Only owner".
   - PC 0xdf=223: Solidity string-store routine (0x3b4) writes the new domain to slot 0.
6. **Behavioral proof (read-only eth_call, never broadcast):**
   - `balanceOf(0x1111..)`: returns `0x..20 00..12 6c622e70726f706572747966696e642e6363`
     = **"lB.propertyfind.cc"** (18 chars) → disguised lookup confirmed, domain at slot 0.
   - `47064d6a("evil.com")` from random 0x1111..: reverts `Only owner` (caller_check).
   - `47064d6a("evil.com")` from owner 0x3a35b409..: succeeds (0x).

## Key Lessons
- Pruned public nodes → fetch runtime code at "latest" (immutable) instead of the pruned block.
- pyevmasm 0.2.x broken → 30-line custom disassembler is faster than debugging it.
- Disguised getters keep the STANDARD selector but their calldata args go unused — trace where SLOAD reads.
- Access control triage = find `CALLER` vs `ORIGIN` opcodes + the `EQ JUMPI`/revert pair; prove with eth_call.
- eth_call is a read-only SIMULATION — safe for read-only CTF rules (no transaction ever broadcast).

## Files
- `disasm_runtime.py` — opcode-table disassembler
- `verify_selectors.py` — eth_call behavioral verification (getter output + setter access control)
- `D:\CTF\data\research\web3\scan2026_bsc_arb.md` — technique notes
