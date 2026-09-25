# BushBash - ⟨⟩⟨⟩ (Misc, 218pts Medium)

## Flag
`bushbash{d1d_y0U_Us3_z3?}`

## Challenge
C++ template obsession: `out.cpp` has 214 `FlagValue<N>` ints (invoked as all-zeros decoy) + 1581 `using Constraint_N = <Template<args>>;` aliases gated by `enable_if_t`. `main()` prints "You got the flag!" only if the struct compiles. Author: Eisverygoodletter.

## Solution
1. Parse the 1581 constraint aliases → translate to Z3:
   - `Equ<c1,c2,t1,V1..V5>` → `c1*V1 + c2*V2 + t1*V3 == V4 + V5` (700)
   - `Lt/Lteq/Gt/Gteq` → inequalities (825)
   - `Divides<A,B>` → `A % B == 0` (56)
2. Z3 on 214 Int vars → **sat**, unique solution
3. Values are ASCII: "...The flag is `bushbash{d1d_y0U_Us3_z3?}`" (filler text added to kill manual solving)
4. Verified: all constraints hold, no alternate solution, and patched file `g++ -fsyntax-only` COMPILES

## Authoring Notes
- Generator: choose 214-char message, emit random constraint templates that hold for it; over-determined system (1581/214) = unique solution
- All-zero FLAGMESSAGE = decoy that can't compile
- Filler prose defeats hand-solving; flag jokes about the intended tool (Z3)
- Compilation is the success oracle (SFINAE `enable_if_t`)

## Lessons
- Template-meta constraints → parse aliases → Z3
- Placeholder/zero data in template-meta = unknown message
- Per-index multiplier bounds (`Fk * m < K`) = printable-ASCII fingerprint
- `FLAGMESSAGE(` appears in both #define and invocation — patch the invocation
