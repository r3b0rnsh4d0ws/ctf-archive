# SCAN2026 — Challenge #5 Flag 8: Radiant Capital UNC Attribution (OSINT + on-chain)

- **Challenge:** SCAN2026 Challenge #5, Flag 8 (175 pts)
- **Task:** The initial compromise began with a macOS backdoor delivered via a fake PDF lure over Telegram. Identify the UNC (Mandiant threat-actor cluster) by combining reconstructed on-chain activity with OSINT. Format `flag{UNC####}`.
- **Flag:** `flag{UNC4736}`
- **Date solved:** 2026-08-02

## Chain of reasoning

### 1. On-chain reconstruction (previous flags of Challenge #5)
- Operator EOA (Flag 3): `0x0629b1048298ae9deff0f4100a31967fb3f98962`
- Attacker backdoor contract (Flag 4): `0x57ba8957ed2ff2e7ae38f4935451e81ce1eefbf5` — deployed dormant 2024-10-02 on 4 chains, activated via Safe-multisig takeover 2024-10-16 (owner of PoolAddressesProvider `0x091d52...`).
- ~$50M drained from Radiant Capital lending pools on Arbitrum + BNB Chain (Flags 4-7).

### 2. OSINT attribution
- Radiant Capital's official **Incident Update (2024-12-06, Medium)** + security partner **Zeal** forensics describe the initial access: on **2024-09-11** a developer received a **Telegram message impersonating a former contractor** asking for feedback on a smart-contract audit, containing a ZIP with a decoy PDF and a **macOS backdoor (INLETDRIFT)** that established persistence.
- **Mandiant** (working with US law enforcement) attributed the attack to **UNC4736** with high confidence of a DPRK nexus. Reported by The Record / Recorded Future (2024-12-11) and Coinedition (2024-12-07).
- **INLETDRIFT** macOS backdoor analysis (Objective-See malware collection; `Penpie_Hacking_Analysis_Report.app` used in the actual Radiant attack, sibling `Amber_OTC_RECEIPT.app`): AppleScript-based dropper, signed with stolen Apple Developer cert ("Ruth Hall" AGN79H7MTU), Apple-notarized, C2 `atokyonews.com`. Attributed to **UNC4736 (also known as AppleJeus or Citrine Sleet)**, DPRK RGB-aligned.

### 3. Disambiguation (anti-trick)
- Candidate **UNC4899** was checked and REJECTED: UNC4899 = TraderTraitor / Jade Sleet / Slow Pisces — a different DPRK actor behind freelance/job-lure and SaaS/cloud supply-chain campaigns (e.g., Google Cloud "North Korea Leverages SaaS Provider", 2026 AirDrop cloud compromise). NOT the Radiant/INLETDRIFT attacker.
- AppleJeus family aliases: UNC4736, Citrine Sleet, Gleaming Pisces, Golden Chollima, Labyrinth Chollima, Nickel Academy, Hidden Cobra (MITRE ATT&CK G1049).

## Result
`flag{UNC4736}`

## Sources
1. Radiant Capital Incident Update — https://medium.com/@RadiantCapital/radiant-capital-incident-update-e56d8c23829e
2. Recorded Future News (The Record) — https://therecord.media/radiant-capital-heist-north-korea
3. INLETDRIFT RE writeup — https://prathameshwalunj.dev/blog/inletdrift/
4. Coinedition (2024-12-07) — Mandiant identified attackers as UNC4736
5. MITRE ATT&CK G1049 (AppleJeus) — https://attack.mitre.org/groups/G1049/
6. CSIDB UNC4736 actor page

## Gotchas
- Google/Bing full-text search are CAPTCHA-walled for headless fetchers; **DuckDuckGo HTML endpoint** (`html.duckduckgo.com/html/?q=...`) works — result titles+snippets suffice for attribution confirmation.
- UNC clusters share aliases across vendors; always disambiguate the two DPRK crypto-theft clusters (AppleJeus/Citrine Sleet = UNC4736 vs TraderTraitor/Jade Sleet = UNC4899).
