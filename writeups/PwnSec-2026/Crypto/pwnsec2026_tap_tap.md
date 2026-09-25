# PwnSec CTF 2026 — tap tap Writeup

**CTF:** PwnSec CTF 2026 | **Category:** Crypto | **Difficulty:** Medium (113 pts)  
**Flag:** `pwnsec{wR17in6_17_t0oK_m3_thRe3__d4y5_d1d_4I_50lv3_i7_1n_thRe3_53c0nDs??}`  
**Technique:** Predicting Truncated Fibonacci Z/(p)-LFSRs via BKZ-20, Resultant GCD, Polynomial GCD, and Kannan's Embedding  

## Summary
An order-$n=25$ Fibonacci LFSR over $\mathbb{Z}_p$ with unknown 128-bit prime $p \approx 2^{128} - \delta$ ($\delta \in [2^{48}, 2^{50}]$), unknown feedback taps $C$, and unknown initial state $A$. Only the top 80 bits of 180 consecutive outputs $A_{25}, \dots, A_{204}$ are given ($Y_i = A_{25+i} \gg 48$).

The solve implements the 4-step framework from the 2023/2024 paper *"An Improved Method for Predicting Truncated Fibonacci LFSRs over Integer Residue Rings"* (Yu et al.):
1. **Lattice Reduction (BKZ-20)**: Construct an $(r+t) \times (r+t)$ lattice with $r=85, t=95$ (dim 180). BKZ-20 (`BKZ_XD`) discovers annihilating polynomials $F^{(0)}, F^{(1)}, \dots$ of degree 84.
2. **Modulus Recovery**: $p^n \mid \text{Res}(F^{(1)}, F^{(2)})$. The GCD of resultants yields $p^{25}$ (3200 bits). The integer 25th root recovers $p = 340282366920938463463374127620052448857$.
3. **Coefficient Recovery**: In $\mathbb{F}_p[x]$, $\gcd(F^{(0)}, F^{(1)}) \pmod p$ yields the degree-25 monic minimal polynomial $f(x) = x^{25} - \sum c_i x^i$, revealing all 25 taps $C$.
4. **Initial State Recovery**: CVP (Kannan's embedding) on a $61 \times 61$ lattice recovers the unknown 48-bit truncated parts of $A_{25}, \dots, A_{49}$ in $<0.01$s. Backward propagation recovers $A_0, \dots, A_{24}$, and SHA-256 + SHAKE-256 decrypts the flag.

## Key Math & Architecture
```text
Lattice: [ 2^80 * I_95    0   ]
         [      Y        I_85 ]

Resultant GCD: gcd(Res(F_0, F_j)) = p^25
p = integer_nth_root(GCD, 25)
f(x) = poly_gcd(F_0, F_1, p) of degree 25
CVP: Kannan's embedding with d=60 relations to recover A[25:50]
```
