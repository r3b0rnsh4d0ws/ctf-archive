# K17 shamir secret spilling — backwards-compat SSS + small-drift lattice recovery

- **CTF:** K17 | **Category:** crypto | **Difficulty:** medium (100)
- **Flag:** `K17{0ur_cl1ent5_r3ally_d0nt_like_r0tating_their_keys!}`
- **Files:** `D:\CTF\ctfs\k17\crypto\shamir-secret-spilling\` (chal.py, out.txt, solvers)

## TL;DR
Legacy poly P (deg 15) and new poly Q (deg 31, Q(0)=FLAG). 16 leaked shares satisfy both (backwards compat); 8 fresh shares satisfy Q only; drift |Q_i - P_i| < B (~253-bit vs 524-bit MOD). Recover P exactly via Lagrange (16 shares, deg-15). Then Q = P_padded + E: 24 linear equations over 32 drift coefficients (rank 24, 8-dim kernel). Small-coefficient bound resolves degeneracy via Kannan embedding + LLL (fpylll/mpfr). Verify all 24 points + bounds, decode Q(0) → flag.

## Lessons
- n shares fully determine a deg-(n-1) poly — compat constraint = n homogeneous equations on the difference.
- Underdetermined linear system + small-coefficient bound = lattice problem.