# CyberStrike 2K26 - AntiDebugAntics (anti-debug bypass / decoy flag)

## Info
- **Category:** Reverse Engineering
- **CTF:** CyberStrike 2K26
- **Flag:** `cyberstrike{deadc0dedeadc0dedeadc0de}`
- **Type:** Anti-debug detection (ptrace + TracerPid + rdtsc timing + cpuid hypervisor) with misdirection

## Files
- `antidebug` — stripped x86-64 PIE ELF (canary, NX, Full RELRO)

## Recon
`.rodata` (0x2000–0x204e) contains only:
```
"r" | "/proc/self/status" | "TracerPid:" | "cyberstrike{deadc0dedeadc0dedeadc0de}"
```
One function of interest: `main` @ 0x1229. No input, no hidden blobs in `.data`/`.bss`.

## Analysis
`main` performs 4 independent anti-debug checks, OR's their results:
1. `ptrace(PTRACE_TRACEME,0,0,0)` → returns -1 when already traced
2. `/proc/self/status` `TracerPid:` parsed with `strncmp`+`strtol` (base 10)
3. `rdtsc` before/after a 1000-iteration delay loop → delta > 5,000,000 cycles (`0x4c4b40`) means a debugger slowed execution
4. `cpuid` leaf 1 → `shr ecx,31` = ECX bit 31 = **hypervisor present** (fires in VMs/WSL2)

The flag-format string is copied from `.rodata` onto the stack. If any check fires,
the 38 bytes are bitwise-NOT'ed before `puts` (non-printable garbage). If all checks
pass, the string prints as-is.

## Exploit
Single-byte patch at 0x1396: `74 15` (`je`) → `EB 15` (`jmp`) forces the clean path
and prints the flag. Equivalent: neutralize any one check (e.g. `seta al` @ 0x138e).

## Key insight
The anti-debug did NOT gate a hidden payload — it only selected between printing the
flag and printing its NOT. Running under gdb or in a VM always yields garbage, which
is the intended misdirection ("leads you astray"). NOT'ing the garbage byte-for-byte
reproduces the exact flag string, confirming the buffer is the flag.

## Lessons
- Anti-debug can be pure misdirection: same buffer, two outputs (plain / NOT)
- CPUID.1:ECX[31] (hypervisor bit) is a common 4th layer that fires on CTF infra VMs
- Diff the two possible outputs to prove the buffer contents
- Branch patch (`je`→`jmp`) is the fastest path bypass in a stripped PIE
