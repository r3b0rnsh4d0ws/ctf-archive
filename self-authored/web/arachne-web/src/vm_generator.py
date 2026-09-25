#!/usr/bin/env python3
"""
VM Challenge Generator - Creates the obfuscated VM binary
"""

import os
import struct
import hashlib
import random

# Custom VM instruction set (32 instructions)
VM_OPS = {
    0x00: 'NOP', 0x01: 'PUSH', 0x02: 'POP', 0x03: 'DUP',
    0x04: 'SWAP', 0x05: 'ADD', 0x06: 'SUB', 0x07: 'MUL',
    0x08: 'DIV', 0x09: 'MOD', 0x0A: 'AND', 0x0B: 'OR',
    0x0C: 'XOR', 0x0D: 'NOT', 0x0E: 'SHL', 0x0F: 'SHR',
    0x10: 'LOAD', 0x11: 'STORE', 0x12: 'LOADI', 0x13: 'STORI',
    0x14: 'JMP', 0x15: 'JZ', 0x16: 'JNZ', 0x17: 'CALL',
    0x18: 'RET', 0x19: 'SYS', 0x1A: 'HALT', 0x1B: 'CMP',
    0x1C: 'JG', 0x1D: 'JL', 0x1E: 'PRINT', 0x1F: 'INPUT',
}

def generate_vm_bytecode():
    """Generate VM bytecode that outputs the fragment2"""
    fragment2 = "4b2a8f1c"  # 8 hex chars
    
    # Convert fragment to bytes
    frag_bytes = bytes.fromhex(fragment2)
    
    # Build bytecode program
    bytecode = bytearray()
    
    # Program structure:
    # 1. Initialize stack
    # 2. Push fragment bytes onto stack (one by one)
    # 3. Print each byte as hex
    # 4. Halt
    
    bytecode.append(0x01)  # PUSH
    bytecode.extend(struct.pack('<I', 0x41414141))  # Dummy value
    bytecode.append(0x1E)  # PRINT
    
    for b in frag_bytes:
        bytecode.append(0x01)  # PUSH
        bytecode.extend(struct.pack('<I', b))
        bytecode.append(0x1E)  # PRINT
    
    bytecode.append(0x1A)  # HALT
    
    return bytes(bytecode)

def encrypt_bytecode(bytecode, key):
    """XOR encrypt bytecode with key"""
    key_bytes = hashlib.sha256(str(key).encode()).digest()
    encrypted = bytearray()
    for i, b in enumerate(bytecode):
        encrypted.append(b ^ key_bytes[i % len(key_bytes)])
    return bytes(encrypted)

def generate_challenge():
    """Generate the RE challenge"""
    key = 0xA7C9B3E2D5F10846  # Derived from crypto challenge
    
    bytecode = generate_vm_bytecode()
    encrypted = encrypt_bytecode(bytecode, key)
    
    # Generate obfuscated Python script
    script = generate_obfuscated_script(encrypted, key)
    
    return {
        'fragment': '4b2a8f1c',
        'bytecode': encrypted.hex(),
        'script': script,
    }

def generate_obfuscated_script(encrypted_bc, key):
    """Generate heavily obfuscated Python script"""
    
    # The script implements the VM in an obfuscated way
    script = f'''
#!/usr/bin/env python3
import sys
import hashlib
import struct

# Obfuscated constants
_0x4A = 0x9E3779B9
_0x2F = 0x517CC1B7
_0x7C = 0x62731158
_0x1A = 0x1F83D9AB

# Encrypted bytecode
_0xBC = {repr(encrypted_bc)}

# Opaque predicate function
def _0x99(x):
    _0x33 = x * 0xCCCCCCCD
    _0x44 = _0x33 >> 32
    _0x55 = _0x44 * 5
    return _0x55 != x

# String decryption (XOR with rotating key)
def _0x77(data, k):
    _0x88 = hashlib.sha256(str(k).encode()).digest()
    _0x99 = bytearray()
    for _0xAA in range(len(data)):
        _0xBB = data[_0xAA] ^ _0x88[_0xAA % len(_0x88)]
        _0x99.append(_0xBB)
    return bytes(_0x99)

# VM execution
def _0x11():
    _0x22 = _0x77(_0xBC, {hex(key)})
    _0x33 = bytearray(_0x22)
    _0x44 = []  # Stack
    _0x55 = 0   # IP
    _0x66 = {{}}  # Memory
    
    while True:
        _0x77_op = _0x33[_0x55]
        _0x55 += 1
        
        if _0x77_op == 0x1E:  # PRINT
            _0x88_val = _0x44.pop()
            sys.stdout.write(chr(_0x88_val))
        elif _0x77_op == 0x1A:  # HALT
            break
        elif _0x77_op == 0x01:  # PUSH
            _0x99_val = struct.unpack('<I', _0x33[_0x55:_0x55+4])[0]
            _0x55 += 4
            _0x44.append(_0x99_val)
        else:
            pass
    
    sys.stdout.flush()

if __name__ == '__main__':
    if _0x99(7):  # Opaque predicate (always true)
        _0x11()
'''
    return script

if __name__ == '__main__':
    data = generate_challenge()
    print("Fragment 2:", data['fragment'])
    print("Bytecode (hex):", data['bytecode'][:64], "...")
