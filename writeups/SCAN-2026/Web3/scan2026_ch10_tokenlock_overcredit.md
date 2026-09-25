# SCAN2026 — Challenge #10: TokenLock over-credit via LegitToken snapshot bug (750 pts)

## Flag
```
flag{0x97f9a35a800f570780f3f41d6fee7f31b0ac50e9|0x9d8c9a6fa2d3657805b66cf54a53c9a5434d2529|0xcf5957e47480cbc1241eeeff9bc5af5ca39ab8ea|0xdf29ebd105758c7c59c721cd136f4108c7c179fa}
```

## Contracts (Base Sepolia)
- TokenLock `0xcabDd74e14d86F5fbd4c81c92841EdfB6e5A2aF5` — verified "TokenLock", solc 0.8.26.
  Functions: `lock(token,amount)`, `unlock(token,sharesToBurn)`, `shares`, `totalShares`,
  `SHARE_PRECISION = 1e18`.
- LegitToken `0x571FD783Ab37629e947920560b277927048204A9` — ERC-1967 proxy →
  implementation `0x8696d80b1bf1ddf29d5555826da69ea7b0fe6fb3` (verified "LegitTokenV5").
  ERC-20 + freeze/freezer/minter/admin and a **first-touch balance-snapshot bug**.

## The accounting flaw
TokenLock share math (exact, from bytecode):
```
lock():   balanceBefore = token.balanceOf(this)
          transferFrom(user, this, amount)
          shares = totalShares==0 || balanceBefore==0 ? 1e18*amount : amount*totalShares/balanceBefore
unlock(): amount = sharesToBurn * token.balanceOf(this) / totalShares
```
A share-based pool is only fair if `balanceOf(this)` reflects real deposits. LegitTokenV5 breaks
that: `_beforeTokenTransfer(account)` snapshots `slot8[account] = slot0[account]` on an account's
**first touch** and flips `touched` (slot7); `balanceOf` returns slot8 once touched, and transfers
keep moving the *other* storage value. Result: after the lock contract is first touched, its
`balanceOf` reads a **stale** balance.

On-chain evidence (reconstructed from the shares math — the shares are stored and authoritative):
- `balanceBefore` for locks #1..#3: 0, 1e11, 2.1e12 (correct).
- `balanceBefore` for locks #4..#7: frozen at **2.1e12** while the real pool grew to 2.6e12
  (deposits of 0cd7, 9d8c, 97f9, cf59, df29 = 5×1e11 were invisible to `balanceOf`).
- `totalShares` kept growing → each locker after the snapshot paid **less than the fair
  1e18 shares/token**, minting inflated shares.

| locker | deposit | shares minted | fair shares | shares/token | result |
|--------|---------|---------------|-------------|--------------|--------|
| e6d8e09e | 1e11 | 1.0000e29 | 1e29 | 1.0000e18 | first, sets price |
| 68053df5 | 2e12 | 2.0000e30 | 2e30 | 1.0000e18 | fair |
| 0cd783e5 | 1e11 | 1.0000e29 | 1e29 | 1.0000e18 | withdrew 98.1% (under) |
| 9d8c9a6f | 1e11 | 1.0476e29 | 1e29 | 1.0476e18 | withdrew 102.8% OVER |
| 97f9a35a | 1e11 | 1.0975e29 | 1e29 | 1.0975e18 | withdrew 107.7% OVER |
| cf5957e4 | 1e11 | 1.1498e29 | 1e29 | 1.1498e18 | withdrew 112.8% OVER |
| df29ebd1 | 1e11 | 1.2045e29 | 1e29 | 1.2045e18 | still holding → can get 118.2% OVER |

Current state (getters): `balanceOf(lock)=2178604952781`, `totalShares=2220451869334279441179343997614`.
Max-unlockable vs deposit for the remaining lockers: e6d8e09e 9.81e10 (under), 68053df5 1.962e12
(under), df29ebd1 **1.1818e11 (OVER)**.

Three 0xC039...-token lockers (d66d, e7f4, e31b) locked the DEX's *other* token — not LegitToken —
excluded.

## How to solve (read-only methodology)
1. **Find the chain**: challenge addresses have no code on Ethereum mainnet; probe EVM chains
   (Base Sepolia has code) — use eth_getCode against ~90 public RPCs.
2. **Source**: contracts verified on sepolia.basescan.org (ABI + bytecode; source not published)
   → read ABI for function layout; disassemble bytecode for storage slots / math.
3. **Events**: keccak topic0 for `Locked(address,address,uint256,uint256)` /
   `Unlocked(address,address,uint256,uint256)`; eth_getLogs in ≤2000-block windows
   (publicnode limit) on Base Sepolia. **Decode data words correctly — offset by the `0x` prefix**
   (a mis-sliced decode initially produced wrong values).
4. **Current state**: call `totalShares`/`shares` getters + `balanceOf(lock)`; cross-validate raw
   mapping slots: `keccak(pad32(key) ++ pad32(slot))`.
5. **Compute over-credit** = (withdrew amount or max-unlockable) minus deposit, per locker;
   collect everyone with positive delta; lexicographic sort of the addresses.

## Key lesson
Share-based lock/vault contracts that read `balanceOf(address(this))` as the value denominator
are exploitable by any token whose `balanceOf` can go stale or be inflated (fee-on-transfer,
snapshot/rebase, blacklist-with-accounting). Always compare each depositor's **shares per token
minted** against the first depositor's rate — a rising rate = over-crediting for later depositors.
