<div align="center">

# R3B0RNSH4D0WS

## BREAK • BUILD • LEARN • REPEAT

**CTF play-by-plays • security research • exploit notes • self-authored challenges**

[![GitHub](https://img.shields.io/badge/GitHub-r3b0rnsh4d0ws-181717?style=for-the-badge&logo=github)](https://github.com/r3b0rnsh4d0ws)
[![CTF Archive](https://img.shields.io/badge/CTF%20Archive-105%20writeups-00ff88?style=for-the-badge&logo=flag)](https://github.com/r3b0rnsh4d0ws/ctf-archive)
[![Categories](https://img.shields.io/badge/10%20categories-8b5cf6?style=for-the-badge&logo=tag)](https://github.com/r3b0rnsh4d0ws/ctf-archive/tree/main/writeups)
[![Self Authored](https://img.shields.io/badge/self--authored-37%20files-d29922?style=for-the-badge&logo=github)](https://github.com/r3b0rnsh4d0ws/ctf-archive/tree/main/self-authored)

</div>

---

## Welcome

This is the public showcase for the R3B0RNSH4D0WS CTF archive: practical writeups, reverse-engineering notes, cryptographic breakdowns, forensic workflows, web attack chains, Web3 investigations, and original challenge work.

The goal is simple: **make the solve path visible**.

Every published writeup is organized by:

```text
CTF → Category → Writeup → Technique → Lesson
```

Browse the complete [writeup index](writeups/README.md), jump into a [category](writeups/README.md), or explore the [self-authored challenge collection](self-authored/).

> **Public-safe by design:** writeups and selected self-authored material are public. Raw third-party challenge files, session cookies/tokens, rejected flags, incomplete work, and oversized artifacts are intentionally excluded. See [publication policy](PUBLICATION.md) and [exclusions](EXCLUSIONS.md).

---

## Archive at a glance

| Metric | Count | What it represents |
|---|---:|---|
| Selected writeups | **105** | Deduplicated public CTF writeups |
| CTF events | **19** | Events represented in the curated public tree |
| Categories | **10** | Browseable technical collections |
| Self-authored files | **37** | Original challenge docs, source, and small artifacts |
| Public tree size | **~686 KB** | Lightweight, linkable, GitHub-friendly archive |
| Raw third-party artifacts | **0** | Excluded from the public repository |

---

## Featured writeups

### SCAN 2026 — Web3 investigation lab

The largest public collection: **40 Web3 writeups** covering fund-flow tracing, token accounting, contract deployment, setter behavior, DEX interactions, exchange withdrawals, laundering paths, and cross-chain cases.

<div align="center">

[![SCAN Web3 collection](https://img.shields.io/badge/SCAN%202026-40%20writeups-8b5cf6?style=for-the-badge)](writeups/SCAN-2026/Web3/)

</div>

**Start here:** [SCAN writeup index](writeups/SCAN-2026/Web3/) · [Web3 category](writeups/Web3.md)

### L3akCTF 2026 — crypto, forensics, pwn, and web

A cross-category set with practical lessons from BabyLCG and classic PRNG recovery, RSA and MQ/Groebner-style cryptanalysis, CT reconstruction, Bosh and VM/reverse paths, and modern web attack chains.

**Browse:** [L3akCTF 2026](writeups/L3akCTF-2026/) · [complete writeup index](writeups/README.md)

### StarPwn 2026 — space, RF, forensics, and stego

A mixed set of PCAP/RF analysis, satellite and orbital concepts, memory/artifact forensics, image steganography, web/space operations, and multi-stage challenge paths.

**Browse:** [StarPwn 2026](writeups/StarPwn-2026/) · [Forensics](writeups/Forensics.md) · [Steganography](writeups/Steganography.md) · [IoT/RF](writeups/IoT.md)

### K17, BushBash, Nexploit, and PwnSec

Focused collections showing reusable patterns: Shamir secret spilling, format strings, ECB/CBC manipulation, vault paths, classical ciphers, web attack chains, LFSR challenges, code-generation injection, and reverse engineering.

**Browse:** [K17](writeups/K17-CTF-2026/) · [BushBash](writeups/BushBash/) · [Nexploit](writeups/Nexploit-Evil-Corp-2026/) · [PwnSec](writeups/PwnSec-2026/)


## Category showcase

| Category | Writeups | What you will find |
|---|---:|---|
| [Crypto](writeups/Crypto.md) | 16 | RSA, AES, CBC/ECB, LFSR, PRNGs, classical ciphers, hash and lattice notes |
| [Forensics](writeups/Forensics.md) | 5 | PCAPs, memory/artifact analysis, satellite and cross-artifact reasoning |
| [IoT / RF](writeups/IoT.md) | 3 | Firmware, radio, satellite, and embedded-system challenge paths |
| [Misc](writeups/Misc.md) | 15 | Encoding chains, pyjails, esolangs, constraint solving, and game logic |
| [OSINT](writeups/OSINT.md) | 1 | Identity, infrastructure, and investigation patterns |
| [Pwn](writeups/Pwn.md) | 7 | Buffer overflows, format strings, ROP, heap, and exploit primitives |
| [Reverse](writeups/Reverse.md) | 7 | VMs, anti-debug, deobfuscation, custom encodings, and binary analysis |
| [Steganography](writeups/Steganography.md) | 2 | LSB, image, audio, and hidden-data techniques |
| [Web](writeups/Web.md) | 9 | Injection, deserialization, authentication, request and application attacks |
| [Web3](writeups/Web3.md) | 40 | Blockchain tracing, DeFi, token flows, RPC verification, and laundering analysis |

**Full index:** [Browse all 105 writeups](writeups/README.md)

---

## Self-authored challenge lab

The archive also contains original challenge work designed for CTF deployment and educational use.

<div align="center">

[![Self-authored challenges](https://img.shields.io/badge/self--authored%20challenge%20lab-d29922?style=for-the-badge&logo=github)](self-authored/)

</div>

### General Skills collection

A set of intentionally awkward but fair challenges:

- `git_blunder` — recover a flag from commit history
- `rabbit_hole_readme` — follow a documented transform chain
- `whitespace_secrets` — decode SPACE/TAB bit encoding
- `recursive_base64` — decode a deep base64 chain
- `tiny_text_svg` — inspect tiny SVG text and ROT13
- `obfuscated_script` — reconstruct a flag at runtime
- `needle_in_haystack` — filter a large log and decode the result
- `the_fine_print` — follow cross-references through a long document

### Multi-stage original work

- [Arachne Web](self-authored/web/arachne-web/README.md) — crypto, reverse, web, forensics, and pwn chained into one challenge.
- [Reverse challenge](self-authored/revchallenge/README.md) — reverse the score gate instead of dumping the flag.

---

## What makes this archive useful

- **Reproducible paths:** each writeup is organized around the reasoning and commands, not just the answer.
- **Reusable techniques:** crypto primitives, exploit patterns, forensic correlations, and investigation workflows.
- **Cross-category indexing:** move from event to category to technique without searching blindly.
- **Negative knowledge included where safe:** failed and partial approaches are preserved when they teach something useful.
- **Provenance:** [PUBLICATION_MANIFEST.csv](PUBLICATION_MANIFEST.csv) records the local source path and SHA-256 for each included writeup.

---

## Explore the archive

<div align="center">

[![Writeups](https://img.shields.io/badge/Writeups-105-00ff88?style=for-the-badge&logo=markdown)](writeups/README.md)
[![Crypto](https://img.shields.io/badge/Crypto-16-8b5cf6?style=for-the-badge)](writeups/Crypto.md)
[![Web3](https://img.shields.io/badge/Web3-40-8b5cf6?style=for-the-badge)](writeups/Web3.md)
[![Forensics](https://img.shields.io/badge/Forensics-5-8b5cf6?style=for-the-badge)](writeups/Forensics.md)
[![Self Authored](https://img.shields.io/badge/Self--authored-37-d29922?style=for-the-badge)](self-authored/)

</div>

- [Complete writeup index](writeups/README.md)
- [Publication policy](PUBLICATION.md)
- [Exclusion rules](EXCLUSIONS.md)
- [Provenance manifest](PUBLICATION_MANIFEST.csv)
- [GitHub organization](https://github.com/r3b0rnsh4d0ws)

---

## Contributing

Want to add a clean, verified writeup?

1. Solve the challenge.
2. Write a reproducible writeup with the key insight, commands, and lessons.
3. Verify the result and check that no private tokens, cookies, infrastructure, or unreleased material are included.
4. Open a pull request against `ctf-archive`.

**Quality over quantity.** Incomplete work stays private until the path, result, and lesson are all clear.

---

<div align="center">

**BREAK • BUILD • LEARN • REPEAT**

*R3B0RNSH4D0WS — public CTF archive and self-authored challenge lab*

</div>


