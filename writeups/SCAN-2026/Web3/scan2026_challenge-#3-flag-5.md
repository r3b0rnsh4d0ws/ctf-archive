# SCAN2026 — Challenge #3 Flag 5 (250 pts) — Count drainer→fee-wallet internal ETH transfers

## Flag
```
flag{747}
```

## Challenge
Wallet-drainer-as-a-service: count direct internal ETH transfers from drainer contract
`0x00000f312c54d0dd25888ee9cdc3dee988700000` to operator fee wallet
`0x9fa7bb759641fcd37fe4ae41f725e0f653f2c726` in the window **2023-04-01T00:00:00Z .. 2024-02-29T23:59:59Z** (UTC, by block timestamp, inclusive).

Counting rules:
- Internal txs only (trace CALL/CREATE/SELFDESTRUCT with value > 0); not the top-level tx, not ERC-20 transfers, not zero-value calls.
- Direct only: immediate sender = drainer, immediate recipient = fee wallet (one hop).
- Successful only: exclude txs that reverted.
- Each qualifying internal transfer counts once even if several occur in the same tx.
- Reference count = number of Etherscan-style internal transactions matching the rules.

## ⚠️ CORRECTION — why the earlier flag{706} was REJECTED
The first solve used **Blockscout v1** `txlistinternal` (3906 address-level rows → 706 after filter) and
"triple-verified" it with Blockscout-only sources. **Blockscout's internal-tx index is INCOMPLETE**:
its own API answered `status:2` + *"Some internal transactions within this block range have not yet been processed"*.
Concretely: for tx `0x44511388...` Blockscout per-tx `txlistinternal` returns "No internal transactions found",
while Etherscan's tx page shows 3 internal CALLs from the drainer (one → fee wallet). All 706 Blockscout rows are
a **subset** of Etherscan's data (0 Blockscout rows are extras). The challenge's reference is
"Etherscan-style" = **Etherscan's own index**, which counts **747**.

## Method (Etherscan ground truth, READ-ONLY)
1. **Exact boundary blocks** (`eth_getBlockByNumber` via `https://eth.rpc.blxrbdn.com`, bloxroute, keyless):
   - start: block 16950602 ts=1680307199 (2023-03-31T23:59:59Z — **1 s BEFORE window**); block 16950603 ts=1680307211 (in window) → first in-window block = **16950603**.
   - end: block 19336606 ts=1709251199 (2024-02-29T23:59:59Z, in window, inclusive) → last = **19336606**.
   - Rows in blocks outside the strict ts window: 0 → boundary handling is a non-issue here.
2. **Drainer-side scrape** — Etherscan UI `https://etherscan.io/txsInternal?a=<drainer>&p=1..84` (50 rows/page, **4,158 rows all-time**, all in-window blocks):
   - Parse each `<tr>`: block, parent tx hash, epoch ts (hidden `showLocalDate` span), type, from (tooltip `data-bs-title`/`title` `(0x…)`), to (`/address/` href), value ETH, success icon.
   - Filter `from`==drainer ∧ `to`==fee wallet ∧ value>0 ∧ ts∈[1680307200,1709251199] → **747 rows**.
   - All 747 rows show the Etherscan green success icon (`fa-check-circle text-success`); 0 failed.
3. **Fee-wallet-side scrape** — `txsInternal?a=<fee wallet>&p=1..150` (**7,466 rows**): same filter → **identical 747**,
   byte-identical `(tx,blk,from,to,eth)` key set (0 miss / 0 extra). Bidirectional confirmation.
4. **Per-tx spot verification** — every one of the 41 rows Blockscout was missing was re-checked on
   `https://etherscan.io/tx/<hash>`: 41/41 = tx Success + exactly one drainer→fee internal transfer (parsed via
   `>Transfer</span>` segments + `data-highlight-target` from/to + `<b>.</b>`-normalized ETH value).

## Results
| Metric | Value |
|---|---|
| Qualifying internal transfers (**Etherscan**) | **747** |
| Distinct txs containing them | 746 |
| txs with >1 qualifying transfer | 1 (`0x6a00d5f7...`, two separate calls, counted twice) |
| Total ETH delivered | 352.84218599054606 ETH |
| First / last transfer | blk 17047048 (2023-04-15) / blk 19233309 (2024-02-15) |
| Blockscout (incomplete index) count | 706 (missing the 41 txs above) |

## Why 706 (the rejected answer) looked right but is wrong
- Blockscout v1 `txlistinternal&address=` returned 3906 rows "complete in one page", and the fee-wallet side
  (3803 rows) agreed at 706 → looked triple-verified.
- The warning `Some internal transactions... not yet been processed` was ignored. Etherscan's index is the
  superset; 41 txs (`0x44511388…`, `0xe53cf023…`, … 41 total) each contain a drainer→fee transfer that
  Blockscout never indexed (per-tx endpoint returns 0 rows).
- Reference wording in the metadata ("Etherscan-style internal transactions", "not the Etherscan UI which
  paginates" = use a flow tool over the SAME index) points at Etherscan's own count: **747**.

## Gotchas
- **Blockscout internal-tx index ≠ complete.** Always check `status`/`message`; a `status:2` + "not yet been
  processed" warning means the address-level listing UNDERCOUNTS. Cross-check against Etherscan's UI/API or
  Tenderly before trusting a count.
- **Etherscan UI pagination**: `txsInternal?a=...&p=N` returns 50 rows/page and shows the total in
  "A total of X internal transactions found". Scrape all pages (84 for drainer, 150 for fee wallet).
- Etherscan row HTML: from-address lives in `data-bs-title`/`title` tooltip `Name&#10;(0x…)`, to-address in
  `/address/` href (EOA rows: both in tooltips); value is `0<b>.</b>2842… ETH` (normalize the dotted span);
  block/tx hrefs use **single** quotes. Epoch is in the hidden `showLocalDate` span.
- Count **rows** not txs: the `0x6a00d5f7...` tx has TWO internal CALLs to the fee wallet (counts twice).
- Boundary trap: `getblocknobytime closest=before` for the start picks block 16950602 whose timestamp is
  **2023-03-31T23:59:59Z** (1 s before the window) — always verify each row's ts, or start from closest=after.

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\f5_es_final.py` — drainer-side Etherscan txsInternal scrape + filter (747)
- `C:\Users\balu\ctf-shared\scan2026\f5_es_fee.py` — fee-wallet-side cross-check (747)
- `C:\Users\balu\ctf-shared\scan2026\f5_verify_extra3.py` — verifies the 41 txs Blockscout misses (41/41)
- `C:\Users\balu\ctf-shared\scan2026\f5_es_matches.json` / `f5_es_fee_matches.json` / `f5_es_matches_status.json`
- `progress.md` (challenge dir)
