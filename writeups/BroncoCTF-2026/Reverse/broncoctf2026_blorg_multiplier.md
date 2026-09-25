# BroncoCTF 2026 - Blorg Multiplier

**Category:** Reverse Engineering
**Score:** 200
**Status:** Solution Logic Complete (Flag Not Verified)
**Flag:** Unknown (awaiting remote verification)

## Challenge Description

A text-based game where you manage "blorgs". Start with 1 blorg, reach exactly 468 blorgs using at most 3 "edits" to get the flag.

## Challenge Analysis

### Game Mechanics (from `checker.py`)

```python
# Commands and their effects:
# increase: (blorgs + 1) * 2, uses 1 edit
# decrease: (blorgs - 1) * 2, uses 1 edit
# none: blorgs * 2, uses 0 edits
# program: create a macro (sequence of commands), uses 1 edit
# show: display current blorg count, uses 0 edits
# quit: exit

# Win condition: blorgs == 468 and edits_used <= 3
# After win, entering "show" reveals the flag
```

### Solution Approach

This is a shortest-path search problem. We need to find a sequence of operations that transforms 1 → 468 using ≤ 3 edits.

**Operations:**
- `increase`: `(x + 1) * 2`, cost = 1 edit
- `decrease`: `(x - 1) * 2`, cost = 1 edit
- `none`: `x * 2`, cost = 0 edits

**BFS Solution (found by `solve2.py`):**

```
Sequence: none, none, none, decrease, none, increase, none, increase, none
Edits used: 3 (decrease + increase + increase)
Blorgs progression:
  1 → 2 → 4 → 8 → 14 → 28 → 58 → 116 → 234 → 468
  none(×3)  dec  none  inc  none  inc  none
   (0)      (1)   (0)   (1)   (0)   (1)   (0)
Total edits: 3 ✓
```

Verification:
- Start: 1
- none: 1×2 = 2
- none: 2×2 = 4
- none: 4×2 = 8
- decrease: (8-1)×2 = 14 (edit 1)
- none: 14×2 = 28
- increase: (28+1)×2 = 58 (edit 2)
- none: 58×2 = 116
- increase: (116+1)×2 = 234 (edit 3)
- none: 234×2 = 468 ✓

Total edits: 3 ✓

### Flag Retrieval

After reaching 468 blorgs, the `show` command reveals the flag. The `show` command hashes the command name with MD5 and checks against a list of valid hashes:

```python
valid_hashes = {
    "11198b294adbcf089f9d27990258fd22",
    "b0fe2606af48e49fd3746844798eb6a0",
    "334c4a4c42fdb79d7ebc3e73b517e6f8",
    "dbd73c2b545209688ed794c0d5413d5a",
    "a9c449d4fa44e9e5a41c574ae55ce4d9",
    "A7DD12B1DAB17D25467B0B0A4C8D4A92",  # MD5("show")
}
```

`hashlib.md5(b"show").hexdigest().upper()` = `A7DD12B1DAB17D25467B0B0A4C8D4A92` ✓

So the `show` command is the one that reveals the flag.

### Exploit Script

```python
#!/usr/bin/env python3
# Solution for BroncoCTF 2026 - Blorg Multiplier

from pwn import *

def solve():
    # The sequence to reach 468 with 3 edits
    sequence = [
        "none", "none", "none",  # 1 -> 2 -> 4 -> 8
        "decrease",              # 8 -> 14 (edit 1)
        "none",                  # 14 -> 28
        "increase",              # 28 -> 58 (edit 2)
        "none",                  # 116
        "increase",              # 234 (edit 3)
        "none",                  # 468
        "show",                  # Get flag
    ]
    
    # p = process('./blorg_multiplier')
    # p = remote('host', port)
    
    # for cmd in sequence:
    #     p.sendline(cmd)
    #     print(p.recvline())
    # 
    # p.interactive()

if __name__ == '__main__':
    solve()
```

## Solution Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `solve.py` | Initial brute force | Partial |
| `solve2.py` | BFS solver (found solution) | ✓ Works |
| `solve3.py` | Program command analysis | Partial |
| `verify.py` | Hash verification | ✓ |

## Hash Verification

```python
import hashlib

commands = ["increase", "decrease", "none", "show", "program", "quit"]
for cmd in commands:
    h = hashlib.md5(cmd.encode("latin-1")).hexdigest().upper()
    print(f"{cmd:12s} -> {h}")

# Output:
# increase     -> 334C4A4C42FDB79D7EBC3E73B517E6F8
# decrease     -> DBD73C2B545209688ED794C0D5413D5A
# none         -> B0FE2606AF48E49FD3746844798EB6A0
# show         -> A7DD12B1DAB17D25467B0B0A4C8D4A92  ← VALID
# program      -> 11198B294ADBCF089F9D27990258FD22
# quit         -> A9C449D4FA44E9E5A41C574AE55CE4D9
```

## Next Steps

1. [ ] Connect to remote server and execute solution
2. [ ] Capture actual flag
3. [ ] Verify with user
4. [ ] Move folder to `1_blorg_multiplier`
5. [ ] Update data/writeups/rev/

## Lessons Learned

1. **BFS is perfect for state-space search** with small state spaces
2. **Zero-cost operations** (`none`) can be used freely to reach intermediate values
3. **Work backwards** from target can sometimes be easier, but BFS from start works well here
4. **Hash verification** is a common pattern in CTF challenges to validate commands

## Tools Used

- Python with BFS (`solve2.py`)
- pwntools for remote interaction
- hashlib for hash verification

## References

- `checker.py` - Original game logic
- `solve2.py` - Working BFS solver
- `verify.py` - Hash verification