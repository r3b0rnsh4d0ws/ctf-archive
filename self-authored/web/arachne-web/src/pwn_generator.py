#!/usr/bin/env python3
"""
Pwn Challenge - Vault Daemon Generator
Creates a vulnerable binary and challenge data
"""

import struct
import os

def generate_vault_daemon():
    """Generate the vulnerable vault daemon source code"""
    
    source = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUF_SIZE 64
#define FLAG_SIZE 16

// Global flag (fragment5)
char FLAG[] = "5a8f3c2dXXXXXXXX";  // X will be replaced

// Vulnerable function
void vulnerable_handler(char *input) {
    char buffer[BUF_SIZE];
    int canary = 0xDEADBEEF;  // Stack canary (simplified)
    
    // Buffer overflow - no bounds checking
    strcpy(buffer, input);
    
    // Check canary
    if (canary != 0xDEADBEEF) {
        printf("Stack corruption detected!\n");
        exit(1);
    }
    
    printf("Processed: %s\n", buffer);
}

// Format string vulnerability for info leak
void diagnostic_mode(char *input) {
    printf(input);  // Format string vulnerability!
    printf("\nDiagnostic complete.\n");
}

// Main service loop
int main(int argc, char *argv[]) {
    char buffer[256];
    
    printf("Arachne Vault Daemon v3.2.1\n");
    printf("Enter command: ");
    
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        return 1;
    }
    
    // Remove newline
    buffer[strcspn(buffer, "\n")] = 0;
    
    // Check for diagnostic mode
    if (strncmp(buffer, "DIAG ", 5) == 0) {
        diagnostic_mode(buffer + 5);
    } else {
        vulnerable_handler(buffer);
    }
    
    printf("Operation completed.\n");
    return 0;
}
'''
    return source

def generate_exploit_hint():
    """Generate hint file for players"""
    return '''
# Vault Daemon Exploitation Guide

## Vulnerability Analysis

The vault daemon has two critical vulnerabilities:

1. **Buffer Overflow** (in `vulnerable_handler`):
   - `strcpy(buffer, input)` with no bounds checking
   - Buffer is 64 bytes, but input can be up to 256 bytes
   - Overwrites return address on stack

2. **Format String** (in `diagnostic_mode`):
   - `printf(input)` with user-controlled format string
   - Can leak stack values including canary and addresses

## Exploitation Strategy

### Step 1: Leak Canary
```
DIAG %08x %08x %08x %08x
```
Find the canary value (0xDEADBEEF or similar pattern) in the output.

### Step 2: Leak Libc Address
Send more format specifiers to leak a libc address (e.g., from the GOT).

### Step 3: Calculate Offsets
- Canary offset: typically 13th stack value
- Libc base: leaked_address - libc_offset
- System address: libc_base + system_offset

### Step 4: ROP Chain
Construct a ROP chain:
- Overwrite return address with `pop_rdi; ret` gadget
- Put "/bin/sh" string address in RDI
- Call system()

### Step 5: Get Shell
Execute the payload to get a shell, then:
```
cat /flag.txt
```
The flag contains fragment5.

## Building the Challenge

```bash
gcc -o vault_daemon vault_daemon.c -no-pie -z execstack -fno-stack-protector
```

Or with full mitigations (harder):
```bash
gcc -o vault_daemon vault_daemon.c
```
'''

def generate_challenge():
    """Generate pwn challenge files"""
    source = generate_vault_daemon()
    hint = generate_exploit_hint()
    
    # Write source
    with open('/tmp/vault_daemon.c', 'w') as f:
        f.write(source)
    
    # Write hint
    with open('/tmp/exploit_guide.md', 'w') as f:
        f.write(hint)
    
    print("Generated vault_daemon.c")
    print("Generated exploit_guide.md")
    
    return {
        'fragment': '5a8f3c2d',
        'source': source,
    }

if __name__ == '__main__':
    generate_challenge()
