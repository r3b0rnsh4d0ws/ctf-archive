# Challenge #6 - Flag 2 (275 pts) — SCAN2026 Tornado Cash withdrawal addresses

## Result
`flag{0x96dc12a1c0f3ad73b9de2e16f88785bac0b6d497|0x54212c9301610ff59a27ca44ae3be827bf0d914d|0xab2b6f1f0032e25b98eb3f68c5d70ee319be45a3|0x8ba0aba87688bad3f58e98fcd1c22eabb6c0c790|0xdc804997502cf7798618161aa8d770a7c4704e04|0xaeca1d64123c410ebe8e73cbedfe9c76babffb2c|0xe315b8d4088c580ea3d4ebe8994857337ef10e6b|0xdccf86d4cf499689d6c3b580e90d77ac6ffab604|0x019004535f0e1fc0ed399bfa7456aebcb57f5d17|0x371e628d2ceb349ddc96beeb74b45e0699d57a31|0x42242156e04db470c26e36cdd3e99fe010063021|0xbe5e23e06cd3ed3d909ff1b8f8d5693b0230b084|0x144cf3dbdd9cf1c07c7a681ef6086f07f60f637b}`

## Method
- Pool 0x910Cbd... (TC 10 ETH) Withdrawal events May 25–Sep 1 2024 via eth_getLogs (tenderly). Event = `Withdrawal(address to, bytes32 nullifierHash, address indexed relayer, uint256 fee)` — only relayer indexed, recipient in data[0:32].
- 13 deposits confirmed (Blockscout txlist of 6 addresses → 13 × 10 ETH to TornadoRouter 0xd90e2f..., blk 20005969..20017786).
- **Key match = timing**: every deposit is followed within 12–39 blocks (~3–8 min) by a pool Withdrawal to a **fresh EOA** (code=0x, nonce=0, balance=0 before). Each of the 13 recipients received exactly ONE pool withdrawal.
- Cross-check: withdraw calldata (selector 0xb438689f, TornadoRouter) recipient == event recipient; tx.to == router; relayer EOA == tx.from.
- All 13 are EOA with nonce 0x0 at dormancy cutoff 19771559.
