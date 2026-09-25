#!/usr/bin/env python3
"""
Arachne's Web - Master Challenge Generator
Generates all challenge artifacts and validates the solution
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from crypto_module import generate_challenge as gen_crypto, generate_cipher_module
from vm_generator import generate_challenge as gen_vm
from forensics_generator import generate_challenge as gen_forensics
from pwn_generator import generate_challenge as gen_pwn

def generate_all():
    """Generate all challenge components"""
    print("=" * 60)
    print("ARACHNE'S WEB - Challenge Generator")
    print("=" * 60)
    
    # Generate crypto challenge
    print("\n[1/4] Generating crypto challenge...")
    crypto_data = gen_crypto()
    print(f"  Fragment 1: {crypto_data['fragment']}")
    
    # Write cipher module (the partial source given to players)
    cipher_src = generate_cipher_module()
    cipher_src = cipher_src.replace(
        'INTERCEPTED_HEX_PLACEHOLDER',
        crypto_data['intercepted']
    ).replace(
        'KNOWN_PLAINTEXT_HEX_PLACEHOLDER',
        crypto_data['known_plaintext']
    )
    with open('dist/cipher_module.py', 'w') as f:
        f.write(cipher_src)
    print("  Written: dist/cipher_module.py")
    
    # Generate VM challenge
    print("\n[2/4] Generating VM challenge...")
    vm_data = gen_vm()
    print(f"  Fragment 2: {vm_data['fragment']}")
    with open('dist/vm_challenge.py', 'w') as f:
        f.write(vm_data['script'])
    print("  Written: dist/vm_challenge.py")
    
    # Generate forensics challenge
    print("\n[3/4] Generating forensics challenge...")
    forensics_data = gen_forensics()
    print(f"  Fragment 4: {forensics_data['fragment']}")
    print("  Written: dist/arachne_vault.pcap")
    print("  Written: dist/memory_dump.raw")
    
    # Generate pwn challenge
    print("\n[4/4] Generating pwn challenge...")
    pwn_data = gen_pwn()
    print(f"  Fragment 5: {pwn_data['fragment']}")
    print("  Written: dist/vault_daemon.c")
    print("  Written: dist/exploit_guide.md")
    
    # Create vault.bin (encrypted container)
    print("\n[*] Creating vault.bin...")
    vault_data = crypto_data['encrypted_vault']
    with open('dist/vault.bin', 'w') as f:
        f.write(f"ENCRYPTED_VAULT:{vault_data}\n")
    print("  Written: dist/vault.bin")
    
    # Write combined flag validation
    fragments = {
        'fragment1': crypto_data['fragment'],
        'fragment2': vm_data['fragment'],
        'fragment3': '4f9c2e87',  # From web challenge
        'fragment4': forensics_data['fragment'],
        'fragment5': pwn_data['fragment'],
    }
    
    full_flag = f"CTF{{arachne_{fragments['fragment1']}_{fragments['fragment2']}_{fragments['fragment3']}_{fragments['fragment4']}_{fragments['fragment5']}}}"
    
    with open('dist/flag.txt', 'w') as f:
        f.write(full_flag + '\n')
    print(f"\n[*] Complete flag: {full_flag}")
    
    # Write writeup
    write_solution(fragments)
    
    print("\n" + "=" * 60)
    print("Challenge generation complete!")
    print("=" * 60)
    
    return fragments

def write_solution(fragments):
    """Write the solution writeup"""
    writeup = '''# Arachne's Web - Solution Writeup

## Flag
`CTF{{arachne_''' + fragments['fragment1'] + '''_''' + fragments['fragment2'] + '''_''' + fragments['fragment3'] + '''_''' + fragments['fragment4'] + '''_''' + fragments['fragment5'] + '''}}`

## Stage 1: The Whispering Oracle (Crypto)

### Vulnerability
The custom stream cipher uses a weak LCG for key derivation. The LCG parameters are:
- a = 0x5DEECE66D
- c = 0xB
- m = 2^48

Given consecutive keystream outputs, we can reverse the LCG to recover the state.

### Solution
1. Take the intercepted ciphertext and known plaintext
2. Compute keystream = ciphertext XOR plaintext
3. Use two consecutive keystream values to reverse the LCG:
   - state_{n-1} = (state_n - c) * a^{-1} mod m
4. Recover the master key from the LCG state
5. Decrypt the vault using the master key

### Fragment 1: `''' + fragments['fragment1'] + '''`

## Stage 2: The Gilded Cage (Reverse Engineering)

### Vulnerability
The VM binary uses control flow flattening and opaque predicates, but the bytecode is only XOR encrypted with a static key derived from the crypto challenge.

### Solution
1. Deobfuscate the Python script
2. Identify the VM implementation
3. Extract the XOR key from the script
4. Decrypt the bytecode
5. Execute the VM to get the output

### Fragment 2: `''' + fragments['fragment2'] + '''`

## Stage 3: The Spider's Den (Web)

### Vulnerability Chain
1. **JWT Algorithm Confusion**: The server accepts tokens with `alg: none`, allowing admin token forgery
2. **SSTI**: The profile page renders user-controlled input as Jinja2 template
3. **Path Traversal**: The upload endpoint saves files with user-controlled paths

### Solution
1. Forge a JWT with `alg: none` and `is_admin: true`
2. Access /admin to get the vault key location
3. Use SSTI in /profile to read the vault_keys table
4. Decode the base64 vault key to get fragment3

### Fragment 3: `''' + fragments['fragment3'] + '''`

## Stage 4: The Silent Channel (Forensics)

### Data Exfiltration
Arachne used DNS tunneling to exfiltrate data. TXT queries to `*.arachne-c2.evil` contain base32-encoded fragments.

### Solution
1. Filter DNS packets in Wireshark (port 53, TXT records)
2. Extract subdomains from queries to arachne-c2.evil
3. Concatenate and decode from base32
4. The decoded data contains fragment4

### Memory Dump
The memory dump has encrypted data at offset 0x123456. The encryption is XOR with a known key.

### Fragment 4: `''' + fragments['fragment4'] + '''`

## Stage 5: The Breaking Point (Binary Exploitation)

### Vulnerabilities
1. **Format String**: `printf(input)` in diagnostic_mode leaks stack values
2. **Buffer Overflow**: `strcpy(buffer, input)` in vulnerable_handler with 64-byte buffer

### Exploitation
1. Connect to the daemon
2. Send `DIAG %p %p %p...` to leak canary and libc address
3. Calculate libc base from leaked address
4. Build ROP chain: `pop_rdi; ret` -> "/bin/sh" -> `system()`
5. Get shell and read /flag.txt

### Fragment 5: `''' + fragments['fragment5'] + '''`

## Complete Flag
```
CTF{{arachne_''' + fragments['fragment1'] + '''_''' + fragments['fragment2'] + '''_''' + fragments['fragment3'] + '''_''' + fragments['fragment4'] + '''_''' + fragments['fragment5'] + '''}}
```
'''
    
    with open('writeup/solution.md', 'w') as f:
        f.write(writeup)
    print("  Written: writeup/solution.md")

def validate_flag(flag):
    """Validate a submitted flag"""
    expected = f"CTF{{arachne_c7a9f2e1_4b2a8f1c_4f9c2e87_9d3e7a2f_5a8f3c2d}}"
    return flag.strip() == expected

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_all()
