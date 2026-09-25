# BushBash — ⟨⟩⟨⟩⟨⟩⟨⟩⟨⟩⟨⟩ (Template Cipher)

**Category:** Reverse Engineering | **Points:** 268 | **Difficulty:** medium | **Solves:** 145
**Author:** Eisverygoodletter
**Flag:** `bushbash{ma5B3_sf1NAe_neXt?}`

## Challenge
Agent sent a coded message: key `[10,21,99,4,534,24,63,57,102,38,0,123,53,674,12,57]`, ciphertext `[221,75,97,125,30,124,51,122,15,186,39,46,74,175,120,83,219,165]`. Attached: `main.cpp` + `<><><><><><>.hpp` — a "horribly obfuscated encryption implementation with lots of templates... nearly nothing in the compiled program."

## Technique: C++ template metaprogramming as a compile-time interpreter
The header is a full compile-time VM in templates:
- `IDXV<N>` int literal · `OWRC<A,B>`/`YVDD` cons-list/nil · `RCYK<v,x>` env binding
- `TWDL<l,N>` nth element · `BJDC<v,env,def>` var lookup · `XBGW<e,env>` evaluator
- Ops: `EPMS`=+, `KZRJ`=*, `RCOB`=%, `QVTC`=^, `CFDD`=list index
- `CWCE<prog,state>` state threading: `JLLV`=assign, `JWTR`=prepend, `ITFH`=save/restore, `HPFP`=repeat N, `KJAT`=sequence

Program: 9 outer iterations; per flag-byte pair `(f[2i], f[2i+1])` run 16 rounds:
```
s = WVTF * (key[j]+1);  z = ((FNHJ + s) * 17) % 135
(RLGL, FNHJ) = (FNHJ, RLGL ^ z)
```
then `WVTF += RLGL + FNHJ`. Output = transformed bytes in order.

## Key insight
`WVTF` only accumulates ciphertext bytes → each pair decrypts backwards independently, no brute force:
```
for j in 15..0: s = WVTF*(key[j]+1); z = ((RLGL+s)*17)%135; (RLGL,FNHJ)=(FNHJ^z,RLGL)
```

## Solve
`solve_tmp_cipher.py` → plaintext `ma5B3_sf1NAe_neXt?`; forward re-encryption matches ciphertext exactly. Flag accepted.

## Lessons
- TMP "encryptors" = compile-time interpreters → translate to a small DSL, don't fight types.
- Feistel-style ciphers invert per-block when round keys derive only from known output.
- Authoring: meaningless struct names + `using` aliases + decoy comments are cheap obfuscation; the design weakness (state = function of ciphertext) is what kills it.

## Files
`D:\CTF\ctfs\2_bushbash\re\2_template_cipher\` (main.cpp, angles.hpp, challenge.zip, solve_tmp_cipher.py, writeup.md, progress.md)
