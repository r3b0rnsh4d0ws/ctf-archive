# srev (K17 2026) — writeup

## Challenge
- **Category:** rev (hard) | **Points:** 216 | **Solves:** 34
- **File:** `srev` — stripped x86-64 ELF, non-PIE, 92KB
- **Description:** runs at 100% CPU for hours with no output.

## Summary
The binary is a "signal-driven VM": native code where each dispatch ends with an
explicit `rt_sigreturn` (syscall 15) restoring a crafted fake signal frame. The
program records at 0x403994 are pre-built signal frames — their fields ARE the
x86-64 register slots. The computation (a counter enumerating 95^12 states) is
designed to run for millions of years. The solve: invert the 236-op bijective
transformation from the all-zeros halt target to recover the root fields = flag.

## Key steps
1. **ptrace tracing** (fork + PTRACE_TRACEME + exec, int3 at 0x4015e0): decoded the
   operand-feeding convention — record[0x90]→RAX (operand), record[0xa8]→RIP
   (opcode), record[0xa0]→RSP, etc. The fake frame is at `rcx-8` (kernel reads rsp-8).
2. **Opcode semantics**: 1=merge, 2=push, 3=dup, 4=pop, 5=ADD, 6=SUB, 7=XOR, 8=ROR,
   9=halt. The a8 field is a return address (record idx+1), not a loop counter.
3. **Halt condition**: fires when the transformation maps root → all-zeros; flag =
   root fields 1-12.
4. **Inversion**: apply the inverse of each ALU op in reverse order from all-zeros.
   Verified: forward transform of the inverse result = all zeros.

## Flag
```
K17{00p$_nO_s1g$}
```

## Files
- `srev` — original binary
- `srev_trace.c`, `srev_trace2.c` — ptrace tracers
- `srev_sim.c` — fast C simulator (verified 100% match with real binary)
- `srev_invert.py` — inversion solver
- `progress.md` — full analysis log

## Lessons
- Signal-frame obfuscation: records double as rt_sigframe register banks.
- ptrace beats static analysis for operand-feeding conventions.
- Invert bijective transformations instead of brute-forcing infeasible computations.