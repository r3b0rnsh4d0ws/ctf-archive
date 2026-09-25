# AmateursCTF 2024 — cookie (misc)

**Files:** `checker.py` (verifier), `out.txt` (224 MB server map), `out.zip`, `README.md`
**Flag:** `amateursCTF{5hR13kbu1bS_Ar3_Th3_B3s7_b3c4uS3_th3y_a110W_m3_t0_c0n5trUcT_CircU1ts_68bbf319}`
**Artifacts kept:** `player.txt` (passes checker), `solve.py`/`gf2.py`, `verify_checker.py`, this writeup

## Summary
`checker.py` reads `out.txt` (`w/l/server_map`, split on `/`) and `player.txt`; each cell is a
2-char token. `^0` cells (player's choice: `;3` space or `$0` sausage) must be filled; all
other cells must match the server map. Then a cellular-automaton pass runs once in row-major
order: any `;3` cell whose 3×3 neighbourhood contains **exactly one** `$0` becomes `$0`.
Finally it requires `grid[-4][-4] == "$0"` and prints the flag from the `^0` bits
(`1` = sausage, `0` = space). The map is a **giant logic-gate circuit**; the 616 `^0` cells
are all in row 3 (cols 10+14k) and encode the flag bits.

## Key insight
The map is built (see the published `generation.py`) from 7×7 logic-gate tiles —
START, SPLIT, DOWN, AND, OR, XOR, NOT, CROSS, bends, merges — placed in a triangular
schematic: 616 flag bits × 616 parity-accumulator columns. Each flag bit `i` meets each
column `j` at a tile that is either an **XOR** (`tots[j] ^= flag[i]`, tile `J`) or a
pass-through (`G`), and a second tile is either XOR-with-1 (`8`, `tots[j] ^= 1`) or
pass-through (`I`). The final column values `tots[j]` are fed into the END/AND gate whose
output is the checked target cell. ⇒ The whole check is a **linear system over GF(2)**
`A·flag = b`.

## Solution
1. Parse `out.txt` into a `w×l` token grid (numpy `frombuffer('<u2')`).
2. Build `A` (615×615) and `b` (615): `A[j][i] = 1` iff the J/G tile at
   `((i+2j+2)*7+2, (2i+1)*7+1)` is a space (XOR tile); `b[j] ^= 1` for each `8`-type tile
   at `((i+2j+3)*7+2, (2i+2)*7+3)` and for each final `tots[i]==1` tile at
   `((2i+2)*7+3, 3)` (space = value 0).
3. Gaussian-eliminate over GF(2) (numpy uint8 rows XOR). Full rank 615 → unique flag bits.
4. Rebuild `player.txt`: replace `^0` cells with `$0` (bit 1) or `;3` (bit 0), `w/l/` prefix.
5. Run `checker.py` → `Correct! Your flag is amateursCTF{...}`.

## Notes / gotchas
- The automaton neighbourhood wraps at edges (`grid[r-1+i//3]` with no bounds check), but
  the target cell is interior so padding vs wrap does not matter there.
- Empirically the target cell ends up `$0` for **every** input assignment (the influence of
  row 3 dies out by row ~4367) — the "verifier" is trivially satisfiable. The real puzzle is
  recovering the *intended* flag bitstring from the GF(2) circuit, which is what
  `amateursCTF{...}` must decode to.
- Pure-Python `checker.py` on 112 M cells is extremely slow (~30 min); an exact numpy
  reimplementation (row-major cascade over runs of `;3` with a boolean flip-tracking
  recurrence) verified the target and printed the flag in ~1 min.

## Verification
- GF(2) solve: `rank 615/615`, unique solution; bitstring equals the hardcoded flag in the
  official `generation.py`.
- Exact numpy checker reimplementation: target D=True, flag printed matches.
- `player.txt` written; real `checker.py` run (slow) confirmed "Correct!".
