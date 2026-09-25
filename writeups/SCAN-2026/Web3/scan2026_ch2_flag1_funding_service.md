# SCAN2026 — Challenge #2 Flag 1: Which service funded the Solana C2 seed?

**Category:** Web3 / Solana blockchain OSINT (read-only) · **Points:** 75
**Date solved:** 2026-08-02 · **Status:** SOLVED

## Flag
```
flag{ChangeNOW}
```

## Challenge
A malware campaign uses Solana transactions as a covert C2 channel (operator encodes C2 server
locations in tx memos; infected machines read via standard Solana RPC). Threat intel identified the
C2 wallet seed address:

```
28PKnu7RzizxBzFPoLp69HLXp9bJL3JFtT2s5QzHsEA2
```

Flag 1 (75 pts): determine which SERVICE funded this seed address.
Submission `flag{SERVICE_NAME}` (no space). Scenario window Oct 2025 – Jun 2026. Explorer: solscan.io.

## Method

### Step 1 — Find the earliest transaction on the seed
Used Solana RPC (`https://api.mainnet-beta.solana.com`), POST JSON-RPC:

```
POST {"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress",
      "params":["28PKnu7RzizxBzFPoLp69HLXp9bJL3JFtT2s5QzHsEA2",{"limit":1000}]}
```

Result: 45 signatures, listed **newest → oldest**; the LAST entry is the OLDEST:

| field | value |
|---|---|
| signature | `3KaXEuGHnNb8nftMtxk19UsJYjfAYqDNPskBcvuC1QrB2QzcSHpnyGKsJfMdYTEKFfDzSGjUShva968UVhV4CdM8` |
| blockTime | 1760536741 → **2025-10-15 13:59:01 UTC** |
| slot | 373544779 |

### Step 2 — Decode the funding transaction
`getTransaction(sig, {"maxSupportedTransactionVersion":0})`:

- System Program `Transfer` from `G2YxRa6wt1qePMwfJzdXZG62ej4qaTC7YURzuh2Lwd3t` to the seed.
- preBalances → postBalances for the seed: **0 → 13,689,670 lamports** = **0.01368967 SOL** (≈ **$1.00** at $73/SOL).
- G2YxRa balance dropped by exactly the same 13,689,670 → it is the direct funder.
- Fee payer `E9vf42zJXFv8Ljop1cG68NAxLDat4ZEGEWDLfJVX38GF` (0.000255 SOL), nonce `DScDQ1zV4…` +
  nonce authority `5n9nx3o8…` — a pre-signed, sponsor-fee (bot/C2-style) transaction.

Note: base58-decoding the raw instruction data gave a nonsense 229k SOL (decode quirk); the
**pre/post balance delta is the authoritative amount**.

### Step 3 — Confirm this is the ONLY funding
Pulled all 45 seed signatures and classified by balance delta + program IDs. Every other tx is a
Memo-program C2 broadcast (e.g. `{"link":"aHR0cDovLzIxNy42OS4zLjIxOC9xUUQlMkZKb2kzV0NXU2s4Z2dHSGlUZGclM0QlM0Q="}`,
fee −5000 lamports, no inbound SOL). So G2YxRa = the service that funded the seed.

### Step 4 — Identify the service behind G2YxRa
Searched the exact address. **PANews / Binance Square** article (2024-10-29, "Shock❗️The Hidden Crisis
of MOODENG on the Solana Chain", by Frank, adapted from PANews) at
`https://www.binance.com/en/square/post/15533493781689` states:

> "The funds for this address come from **G2YxRa6wt1qePMwfJzdXZG62ej4qaTC7YURzuh2Lwd3t**, which has
> been involved in several rug events on social media. Some views suggest that this address is
> **sourced from ChangeNOW's hot wallet**, which had previously been used multiple times for hacking
> attacks."

Corroboration: G2YxRa is a very old, extremely high-volume wallet (hundreds of thousands of txs,
~3k–8k txs/day since before the campaign window) — consistent with an exchange/swap hot wallet.
ChangeNOW is an instant, no-KYC swap service (a favored on-ramp for threat actors), and the funding
amount was ≈ exactly $1.00 — consistent with a minimum instant-swap funding of the C2 wallet.

## Answer
The service that funded the seed address is **ChangeNOW** → **`flag{ChangeNOW}`**

## Files kept
- `C:\Users\balu\ctf-shared\scan2026\solve_c2f1.py` — reusable solver/evidence script
- `C:\Users\balu\ctf-shared\scan2026\solana_rpc.ps1` — Solana RPC wrapper w/ retry
- `C:\Users\balu\ctf-shared\scan2026\seed_txs.txt`, `tx1_raw.json`, `decode_funding*.py` — evidence
- `D:\CTF\ctfs\0_scan2026\challenges\challenge-#2-flag-1\progress.md`
- Research: `D:\CTF\data\research\osint\scan2026_explorers.md` (Solana funding attribution section)

## 2026-08-03 addendum (independent re-verify)
Second independent source corroborates the attribution:
- odinbot.io "How to Reverse ChangeNOW & SimpleSwap.io Transactions":
  "For SOLANA transactions, both ChangeNOW and SimpleSwap use the same main wallet address:
   G2YxRa6wt1qePMwfJzdXZG62ej4qaTC7YURzuh2Lwd3t. This wallet exclusively handles SOLANA transactions."
=> flag{ChangeNOW} confirmed. Solver: C:\Users\balu\ctf-shared\scan2026\solve_c2f1.py
