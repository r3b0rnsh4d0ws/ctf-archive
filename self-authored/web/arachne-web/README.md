# Arachne's Web - CTF Challenge

## Overview

**Difficulty:** Insane / Expert+
**Category:** Multi-Stage (Crypto + RE + Web + Forensics + Pwn)
**Flag format:** `CTF{arachne_f1_f2_f3_f4_f5}`

Arachne's Web is a multi-stage CTF challenge combining five distinct exploitation vectors. Players must unravel each strand of the labyrinth to extract five 8-character hex fragments and combine them into the complete flag.

---

## Quick Start

### Prerequisites
- Python 3.8+
- Flask (`pip install flask pyjwt`)
- Wireshark/tshark (for forensics)
- gcc (for pwn challenge compilation)
- Python scapy (for pcap analysis)

### Deploy the Challenge

```bash
# 1. Install dependencies
pip install flask pyjwt scapy

# 2. Start the web challenge server
python src/web_challenge.py
# Server runs on http://0.0.0.0:9000

# 3. (Optional) Compile the pwn challenge
gcc -o dist/vault_daemon dist/vault_daemon.c -no-pie -z execstack -fno-stack-protector
```

### Challenge Files

All player-facing files are in `dist/`:

| File | Description |
|------|-------------|
| `challenge.md` | Challenge description |
| `cipher_module.py` | Partial crypto module source (with flaws) |
| `vault.bin` | Encrypted vault container |
| `vm_challenge.py` | Obfuscated VM binary challenge |
| `arachne_vault.pcap` | Network capture with DNS tunneling |
| `memory_dump.raw` | 4MB process memory dump |
| `vault_daemon.c` | Vulnerable daemon source code |
| `exploit_guide.md` | Exploitation hints |

---

## Challenge Architecture

### Stage 1: The Whispering Oracle (Crypto)
- **Type:** Cryptanalysis
- **Difficulty:** Hard
- **Skills:** LCG analysis, stream cipher cryptanalysis, differential cryptanalysis
- **Goal:** Recover the master key from intercepted keystream, decrypt `vault.bin`

### Stage 2: The Gilded Cage (Reverse Engineering)
- **Type:** Binary RE / Code Analysis
- **Difficulty:** Hard
- **Skills:** Deobfuscation, VM analysis, Python reverse engineering
- **Goal:** Deobfuscate `vm_challenge.py`, execute the VM, extract fragment

### Stage 3: The Spider's Den (Web Exploitation)
- **Type:** Web / Chain Exploitation
- **Difficulty:** Hard
- **Skills:** JWT manipulation, SSTI, path traversal, chaining vulnerabilities
- **Goal:** Exploit the web service at `http://localhost:9000` to extract fragment

### Stage 4: The Silent Channel (Forensics)
- **Type:** Forensics / Network Analysis
- **Difficulty:** Medium-Hard
- **Skills:** PCAP analysis, DNS tunneling detection, base32 decoding, XOR decryption
- **Goal:** Extract hidden data from `arachne_vault.pcap` and `memory_dump.raw`

### Stage 5: The Breaking Point (Binary Exploitation)
- **Type:** Pwn / Binary Exploitation
- **Difficulty:** Hard
- **Skills:** Format string exploitation, buffer overflow, ROP, canary bypass
- **Goal:** Exploit `vault_daemon` to get shell and read the flag

---

## Flag Validation

The complete flag is:
```
CTF{arachne_c7a9f2e1_4b2a8f1c_4f9c2e87_9d3e7a2f_5a8f3c2d}
```

Each fragment:
- `c7a9f2e1` - From crypto analysis
- `4b2a8f1c` - From VM execution
- `4f9c2e87` - From web exploitation
- `9d3e7a2f` - From forensics analysis
- `5a8f3c2d` - From binary exploitation

---

## Technical Details

### Crypto Module
- Custom 4-round Feistel network
- Weak LCG-based key schedule (predictable)
- Related-key vulnerability in round key derivation
- Players must perform LCG state recovery + differential cryptanalysis

### VM Challenge
- 32-instruction custom stack VM
- XOR-encrypted bytecode
- Control flow flattening
- Opaque predicates
- Encrypted string literals

### Web Challenge
- Flask-based web service
- JWT algorithm confusion (`none` algorithm)
- Jinja2 SSTI in profile rendering
- Path traversal in file upload
- SQLite backend

### Forensics
- DNS tunneling via TXT records
- Base32-encoded exfiltration
- ICMP steganography
- XOR-encrypted memory artifacts

### Pwn Challenge
- Stack buffer overflow
- Format string information leak
- Stack canary bypass
- ROP chain to `system('/bin/sh')`
- Requires reading `/flag.txt`

---

## Development

### Regenerate All Challenge Files

```bash
python generate_all.py
```

This will regenerate all challenge artifacts with new random fragments and keys.

### Test the Web Challenge

```bash
python src/web_challenge.py
# Visit http://localhost:9000
```

### Verify Solutions

```bash
python generate_all.py  # Shows all fragments
python -c "from generate_all import validate_flag; print(validate_flag('CTF{arachne_c7a9f2e1_4b2a8f1c_4f9c2e87_9d3e7a2f_5a8f3c2d}'))"
```

---

## Writeup

The complete solution writeup is in `writeup/solution.md`. It is intended to be published after the CTF ends.

---

## License

Educational use only. For CTF purposes.
