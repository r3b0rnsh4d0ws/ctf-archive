#!/usr/bin/env python3
"""
Forensics Challenge Generator
Creates pcap with DNS tunneling and steganography, plus memory dump
"""

import struct
import os
import random
import hashlib
import base64
from scapy.all import *

def generate_dns_tunneling_pcap():
    """Generate pcap with DNS tunneling data exfiltration"""
    packets = []
    
    # The hidden message (base32 encoded)
    secret = b"FRAGMENT4_KEY:9d3e7a2f"
    secret_b32 = base64.b32encode(secret).decode().lower()
    
    # Split into chunks of ~10 chars each for subdomain labels
    chunks = []
    for i in range(0, len(secret_b32), 10):
        chunks.append(secret_b32[i:i+10])
    
    # Malicious domain
    domain = "arachne-c2.evil"
    
    # Generate DNS queries
    for i, chunk in enumerate(chunks):
        # Randomize timing (1-3 seconds between queries)
        time_offset = i * random.uniform(1.0, 3.0)
        
        # DNS query with data in subdomain
        full_domain = f"{chunk}.{domain}"
        pkt = IP(dst="10.0.0.1")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=full_domain, qtype="TXT"))
        packets.append((time_offset, pkt))
    
    # Add some decoy traffic
    for i in range(20):
        time_offset = random.uniform(0, 60)
        decoy_domain = random.choice([
            "google.com", "cloudflare.com", "github.com",
            "stackoverflow.com", "microsoft.com"
        ])
        pkt = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=decoy_domain, qtype="A"))
        packets.append((time_offset, pkt))
    
    # Add ICMP packets with steganographic payloads
    icmp_key = b"XORKEY2024"
    for i in range(10):
        time_offset = random.uniform(0, 60)
        # Hidden data in ICMP payload
        hidden = bytes([random.randint(0, 255) for _ in range(32)])
        hidden_xor = bytes(a ^ b for a, b in zip(hidden, icmp_key * (len(hidden) // len(icmp_key) + 1)))
        pkt = IP(dst="10.0.0.2")/ICMP()/Raw(load=hidden_xor)
        packets.append((time_offset, pkt))
    
    # Sort by time
    packets.sort(key=lambda x: x[0])
    
    # Write pcap
    wrpcap('/tmp/arachne_vault.pcap', [p for _, p in packets])
    print(f"Generated pcap with {len(packets)} packets")
    
    return secret_b32

def generate_memory_dump():
    """Generate a raw memory dump with embedded data"""
    # 4MB memory dump
    dump_size = 4 * 1024 * 1024
    dump = bytearray(os.urandom(dump_size))
    
    # Embed encrypted flag fragment at specific offset
    fragment4 = "9d3e7a2f"
    fragment_bytes = fragment4.encode()
    
    # XOR encrypt with key
    xor_key = b"VMEMORYKEY2024"
    encrypted = bytes(a ^ b for a, b in zip(fragment_bytes, xor_key[:len(fragment_bytes)]))
    
    # Embed at offset 0x123456 (chosen to be realistic)
    offset = 0x123456
    dump[offset:offset+len(encrypted)] = encrypted
    
    # Also embed some readable strings (to simulate real memory)
    strings = [
        b"arachne_vault_daemon",
        b"libc.so.6",
        b"/flag.txt",
        b"password123",
        b"AES-256-GCM",
        b"vault_key.dat",
    ]
    
    for s in strings:
        pos = random.randint(0, dump_size - len(s))
        dump[pos:pos+len(s)] = s
    
    # Write memory dump
    with open('/tmp/memory_dump.raw', 'wb') as f:
        f.write(dump)
    
    print(f"Generated memory dump ({len(dump)} bytes)")
    print(f"Fragment4 embedded at offset 0x{offset:X}")
    
    return fragment4

def generate_challenge():
    """Generate all forensics challenge files"""
    secret = generate_dns_tunneling_pcap()
    fragment = generate_memory_dump()
    
    # Move to dist directory
    os.system('cp /tmp/arachne_vault.pcap dist/arachne_vault.pcap')
    os.system('cp /tmp/memory_dump.raw dist/memory_dump.raw')
    
    return {
        'fragment': '9d3e7a2f',
        'dns_secret': secret,
    }

if __name__ == '__main__':
    generate_challenge()
