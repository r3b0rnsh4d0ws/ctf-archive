# Challenge #1 - Flag 2 (200 pts) — SCAN2026

## Result
`flag{0xdd6980fe48ffc84dce29b162affbb7438bac4d8894d9941a195bdf98c97b0b48|0xe4ab1e4e895ecc528dee0c6b18ceacd33ae9ff28|0xcc6ae8425deedfdc6941f3eab119493be5c1117d|308529865406|308529865405|166923566471660937170|167002900000000000000}`

## Trail (continuation of Flag 1)
- C = 0xf600c14e09c8997851b732d079d3b8e7b357980b (USDT consolidator from Flag 1).
- C sent ETH (direct native transfers, 2022-11-23) to 2 branches ≥100 ETH: **B1** 0x417590Eeda96d5F749bd6c4910e33706321eFAd4 (152 ETH), **B2** 0x0485b598855Be38E38bcFC49922f6dbDd907026d (152.9742 ETH).
- Funding: B2 sent **308,529,865,406 USDT** (raw, >300000e6) to **S** = 0xe4ab1e4e895ecc528dee0c6b18ceacd33ae9ff28 (fresh EOA) at blk 17097057 (tx 0x7c4b1e5e...).
- S swapped USDT→WETH on Uniswap V3 router 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B (tx 0xdd6980fe..., blk 17097107): in 308,529,865,405 USDT, out **166.9236 WETH** (Withdrawal log src==Q.to).
- S forwarded **167.0029 ETH** to dormant EOA 0xcc6ae8425deedfdc6941f3eab119493be5c1117d (code=0x, nonce=0 at 19771559) within 128 blocks of the swap.

## Technique summary
- **Branches**: direct native transfer filter (from=C, input=0x, value>0, status=ok) via Blockscout v2 txlist.
- **Funding log**: eth_getLogs USDT Transfer, topic[1] (sender) filtered per branch; select greatest raw; verify tx.from==branch & recipient EOA at log block.
- **Swap candidate**: for each S-tx after F, sum USDT-transfer logs from S (INPUT_RAW) and WETH Withdrawal wads with src==Q.to (WETH_OUT_WEI); require 300000e6 < INPUT_RAW <= FUNDING_RAW and WETH_OUT > 160e18.
- **Dormancy**: eth_getCode / eth_getTransactionCount at block 19771559 must be 0x / 0.
- **Selection**: smallest non-negative FUNDING_RAW - INPUT_RAW.
