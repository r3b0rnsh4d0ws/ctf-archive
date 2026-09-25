# SCAN2026 — Challenge #6 Flag 3 (200 pts): Tornado Cash intermediary

**Status: SOLVED** — Flag: `flag{0xcab3359f621c719fc8458584b378823a48b6fbb1}`

## Brief
Ethereum mainnet, June 2024. Threat actor launders stolen crypto via Tornado Cash
(10-ETH pool, withdrawals via TornadoRouter relayer 0xd90e2f925DA726b50C4Ed8D0Fb90AD053324F31b).
Flag 2 gave the 13 withdrawal-recipient addresses. Flag 3 asks for the INTERMEDIARY
address whose activity connects the withdrawal addresses with the depositing addresses.

## The laundering loop (fully traced)
```
THORChain Router 0xd37bbe5744d7... (internal transfers ~19.75 ETH)
        |  (blk 20009853..20010252)
        v
[6 depositors] --13x10 ETH TC deposits--> TornadoRouter
        |                                     |
        |  funding: 0xcab3359f -> E938 19.776 ETH (blk 20010346)
        |  (other funders: d751A968/B52b36e4/D567bBEf/Ade20932/1F8C037b/4Fef0026/6D5C3408)
        v                                     v
                                    13 withdrawal addresses (fresh EOAs)
                                           |   main: ~9.9 ETH each -> KyberSwap 0xFc99f58A
                                           |        (swapBridgeToV2 ETH->USDT, USDT->0xDd888469
                                           |         EOA, SwftSwap bridge -> TRON USDT)
                                           |   dust: WDs1-4 -> 0xcab3359f (blk 20009632-46)
                                           |         WDs5-13 -> 0xE43fEd4
                                           v
                                   0xcab3359f  <== INTERMEDIARY (pivot back to depositors)
```

## Key finding
**`0xcab3359f621C719fC8458584b378823a48b6Fbb1`** (EOA) is the only address that both
- RECEIVES from withdrawal addresses: dust from WDs 1-4 (0x96dc12a1, 0x54212c93,
  0x8ba0aba8, 0xab2b6f1f — the exact recipients of the D877+32d2 deposits), and
- CONNECTS to depositing addresses: sends 19.776280 ETH to depositor
  0xE938B5f92451e6237E224b506FCf8B1107b31454 (blk 20010346, 09:17:11), which then
  makes the next 2x10 ETH TC deposits (blk 20010369 / 20010403).

So the WDs' leftovers return into the next deposit round through this single pivot.
The 19.776 balance itself was funded via internal transfers from the THORChain Router
0xd37bbe5744d7... (5 transfers, blk 20009853-20010252) — THORChain is the attacker's
cross-chain on-ramp (internal forwards never show in the recipient's top-level txlist).

## Why the other common recipients are NOT the answer
- `0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f` (KyberSwap aggregator proxy,
  TransparentUpgradeableProxy, impl 0x9bc5a2d6..., selector 0x3d21e25a
  swapBridgeToV2): receives from ALL 13 WDs but is a public DEX aggregator — zero
  direct depositor links. It is the exit ramp, not the intermediary.
- `0xE43fEd4Add1502C33dCf16Cb2F27d81d3D1762Bf`: receives dust from 9 WDs but never
  touches any depositor (only sweeps 0.098 ETH to 0x137c65B5 on Jun 6).
- `0xDd888469ddEC98e2ba00d38a9BEb557e86C1CF60`: USDT sink EOA, 0 transactions
  ever (only ERC20 inflows), no depositor link.

## Techniques worth remembering
1. **Don't stop at the biggest common recipient.** A DEX-aggregator/router is a
   trivially "common" recipient that thousands of users share — check whether its
   activity actually links to the other side of the brief (depositors). The real
   intermediary can be the *dust* recipient that doubles as a deposit funder.
2. **Dust sweeps reveal ownership.** Fresh laundering addresses sweep their leftover
   gas/fee dust to the operator's control addresses. Map dust recipients and check
   whether they also fund the depositor cluster.
3. **Internal transfers hide real funding.** EOAs funded via contract-internal
   forwards (THORChain Router, etc.) show 0 matching txs in their own txlist. Use
   Blockscout v1 `txlistinternal&address=` + archive `eth_getBalance` at exact
   blocks to find the true source.
4. **swapBridgeToV2 (0x3d21e25a) = KyberSwap aggregator.** Decoded request tuple
   (srcToken, destToken, destAddress, ...) reveals the token exit and destination;
   "USDT(TRON)" + T... address in payload = SwftSwap/THORChain-style cross-chain exit.
5. **Deposit funding correlation:** fetch each depositor's txlist; funders that
   appear right before deposits (19.776 ETH -> E938) + dust recipients from WDs =
   the intermediary bridge.
