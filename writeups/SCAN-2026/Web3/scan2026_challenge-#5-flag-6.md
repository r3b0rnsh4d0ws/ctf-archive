# SCAN2026 — Challenge #5 Flag 6 (125 pts) — Radiant Capital Arbitrum admin multisig signer removals

## Flag
```
flag{3}
```

## Task
From the takeover tx `0x7856552db409fe51e17339ab1e0e1ce9c85d68bf0f4de4c110fc4e372ea02fb1` (Arbitrum),
identify the protocol's Arbitrum ADMIN MULTISIG (the Safe whose owners are the administrative signers).
On 2024-10-16 (UTC) count how many DISTINCT signer addresses were REMOVED from that Safe through
owner-management transactions (removeOwner, or the outgoing owner of a swapOwner). Count each removed
signer once; do NOT count added or replacement signers.

## Result: 3 distinct signers removed on 2024-10-16 → `flag{3}`

## Method (read-only)

### 1. Identify the admin multisig
From Flag 4: the takeover tx's `multicall` data[0] called `execTransaction` **on** the Gnosis Safe
`0x111ceeee040739fd91d29c34c33e6b3e112f2177` with `to = PoolAddressesProvider 0x091d52...`,
`data = transferOwnership(0x57ba8957...)`. The PoolAddressesProvider's previous owner was
`0x111ceeee...` → that Safe is the protocol's **Arbitrum admin multisig**.
- Safe implementation = **GnosisSafeL2** `0x3E5c63644E683549055b9Be8653de26E0B4CD36E`
  (Blockscout / storage slot 0). Confirmed events `SafeMultiSigTransaction` (0x66753cd2) +
  `ExecutionSuccess` (0x442e715f) in the takeover receipt.

### 2. Correct event topics (gotcha)
Modern Safe owner events are `AddedOwner(address)` = `0x9465fa0c…` and
`RemovedOwner(address)` = `0xf8d49fc5…`. The flag brief's "OwnerAdded (0x9465fa0c…)" label is wrong —
0x9465fa0c is keccak of `AddedOwner(address)` (legacy GnosisSafe used `OwnerAdded`/`OwnerRemoved`).
Compute topics locally (pycryptodome keccak; validated vs keccak256("")=0xc5d24601…).
These events are **non-indexed** → the owner address is in log `data`, not topics[1].

### 3. Get logs (public RPC eth_getLogs is broken)
`arb1.arbitrum.io/rpc` `eth_getLogs` silently returns `[]` even for blocks with known Safe logs
(verified against the takeover block). Use **Blockscout v2**:
`GET https://arbitrum.blockscout.com/api/v2/addresses/{safe}/logs` — paginate with
`index` + `block_number` (descending) from 2026 back until block < 264231580 (2024-10-16 00:00 UTC).
Filter items by `block_timestamp` date == 2024-10-16.

### 4. Findings for 2024-10-16 (UTC)
Exactly **3 `RemovedOwner` events**, each from its own `execTransaction` whose inner calldata selector
was `0xf8dc5dd9` = `removeOwner(address prevOwner, address owner, uint256 newThreshold)`:

| Time (UTC) | Block | tx | Removed signer |
|---|---|---|---|
| 21:48:30 | 264543801 | `0x6d8a884925f229bcc62444af1a7fc68ce68cbf5e961a1db987be549890b4e648` | `0x20340c2a71055FD2887D9A71054100FF7F425BE5` |
| 21:49:43 | 264544087 | `0x93ebef402869c97738837efa0a3f4c1117b5c22afabce220fd17c0753345771f` | `0x83434627e72d977af18F8D2F26203895050eF9Ce` |
| 22:09:43 | 264548878 | `0x4ae7c216e3320560ff50b696bc2bfa726c29e6a4dba3c5d7abecb3bd8c574345` | `0xbB67c265e7197A7c3Cd458F8F7C1d79a2fb04d57` |

- **Zero `AddedOwner` events and zero `swapOwner`** (swapOwner would emit Added+Removed) on Oct 16.
- Drain tx was 17:09:18Z; these removals (21:48–22:09Z) are the protocol's response revoking the 3
  compromised signers ("revoked the compromised signers' access" per the brief).
- The full owner reset (8 removals + 4 additions) occurred **2024-10-17** — outside the window, not counted.

### 5. Count
Distinct removed addresses: 3 → `flag{3}`.

## Cross-checks
- Safe transactions endpoint (`/api/v2/addresses/{safe}/transactions`, paginated with
  `block_number,index,items_count,inserted_at,value,hash`) shows exactly 3 execTransaction txs on Oct 16.
- All 3 txs emit `ExecutionSuccess` (executed, not reverted).
- Events present: 3 × `RemovedOwner` + 3 × `SafeMultiSigTransaction` + 3 × `ExecutionSuccess`
  (plus the 2 takeover-block events) = complete for the day.

## Files
- Solver: `C:\Users\balu\ctf-shared\scan2026\flag6_solve.py` (also copied to challenge dir)
- Full decoded Oct-16 logs: `flag6_oct16_logs.py` output
- Owner events (2024-2026 window): `owner_events_all.json`
- Progress: `D:\CTF\ctfs\0_scan2026\challenges\challenge-#5-flag-6\progress.md`
