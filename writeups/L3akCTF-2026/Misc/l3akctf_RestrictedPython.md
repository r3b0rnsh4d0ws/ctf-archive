# L3akCTF 2026 - Is RestrictedPython Actually Restricted? (Challenge #3)

## Challenge Info
- **Category:** Misc
- **Difficulty:** Hard
- **Status:** UNSOLVED (local analysis only - server was down)
- **Files:** `chall.zip` containing `chall.py`

## Source Code Analysis

The challenge runs RestrictedPython v8.4 with a tight configuration:

```python
namespace = safe_globals.copy()
namespace.update({
    "__name__": "0x1622",
    "__metaclass__": type,          # Real Python type injected!
    "_getattr_": safer_getattr,     # Blocks _ prefixed + INSPECT_ATTRIBUTES
    "_getitem_": default_guarded_getitem,
    "_getiter_": default_guarded_getiter,
    "_print_": PrintCollector,
    "_write_": full_write_guard,    # Wraps non-safe objects in Wrapper
})
exec(code, namespace, namespace)
```

**Flag check:** After exec, reads `/flag.txt` and checks if it appears in PrintCollector output.

## Restrictions Identified

### 1. `compile_restricted` AST-level blocks:
- ALL `_` prefixed variable names → SyntaxError
- ALL `_` prefixed attribute access → SyntaxError
- `metaclass=` keyword in class defs → SyntaxError
- `print` as variable name → SyntaxError
- `import` compiles but `__import__` not in builtins

### 2. `safer_getattr` runtime blocks:
- `name.startswith('_')` → AttributeError
- `name in INSPECT_ATTRIBUTES` → AttributeError (gi_frame, f_back, f_builtins, etc.)
- Blocks str.format, string.Formatter methods

### 3. `full_write_guard` / `Wrapper`:
- ALL attribute assignment on non-safe objects → TypeError: "attribute-less object"
- Only `list` and `dict` are safetypes (not wrapped)
- `Wrapper.__setattr__` and `__delattr__` always raise

### 4. `guarded_setattr` (replaces real `setattr` in builtins):
- Wraps object with `full_write_guard` before calling `setattr`
- So even `setattr(obj, name, val)` fails for custom objects

### 5. Safe builtins (NO access to):
- `getattr`, `type`, `object`, `open`, `exec`, `eval`, `compile`
- `__import__`, `__build_class__` (accessible only via compiler-generated code)
- `dir`, `vars`, `globals`, `locals`, `property`, `staticmethod`
- `list`, `dict`, `set` (can't call constructors, but `{}` literal works)

### Available builtins:
```
abs, bool, bytes, callable, chr, complex, delattr, divmod, float, 
hash, hex, id, int, isinstance, issubclass, len, oct, ord, pow, 
range, repr, round, setattr, slice, sorted, str, tuple, zip
```

## Key Discoveries

### CVE-2023-37271 (gi_frame exploit) - PATCHED
```python
# This exploit does NOT work in v8.4:
g = (g.gi_frame.f_back for x in [1])
[x for x in g][0].f_back.f_back.f_builtins["__import__"].system("cat /flag.txt")
```
- `gi_frame`, `f_back`, `f_builtins` are ALL in `INSPECT_ATTRIBUTES` frozenset
- `safer_getattr` blocks them at runtime AND `compile_restricted` blocks at compile time

### `__metaclass__` injection
- `visit_ClassDef` transformer rewrites every class to `class X(metaclass=__metaclass__)`
- This means `type` is injected into every class through the namespace
- But user code CANNOT reference `__metaclass__` (compiler blocks `_` prefix)

### Unicode identifier bypass
- `U+02CD` (ˍ, MODIFIER LETTER LOW MACRON) bypasses both:
  - `compile_restricted` name check (doesn't start with `_`)
  - `safer_getattr` check (doesn't startswith `_`)
- But only allows creating new variables, not accessing `_` prefixed namespace entries

### `setattr` is NOT real `setattr`
- `safe_globals['__builtins__']['setattr']` is `guarded_setattr`, NOT builtin `setattr`
- `guarded_setattr` wraps objects with `full_write_guard` → Wrapper
- `Wrapper.__setattr__` always raises TypeError

## What Didn't Work
1. `gi_frame` exploit (CVE-2023-37271) - fully patched
2. `try/except*` exploit (CVE-2025-22153) - patched in v8.0
3. Unicode identifier bypass - allows new vars but no namespace access
4. `setattr` bypass - guarded_setattr wraps objects
5. `__build_class__` indirect access - compiler blocks `_` names
6. Exception frame leaking - `__traceback__` blocked
7. Function `__globals__` access - `__globals__` blocked
8. Class `__dict__` access - `__dict__` blocked
9. Descriptor protocol - `__get__`/`__set__` blocked
10. Context managers - `__enter__`/`__exit__` blocked

## Possible Remaining Approaches (NOT TESTED)
1. **`class` with `*args`/`**kwargs`** - might bypass keyword checks
2. **Decorator chain** - capturing namespace through decorator
3. **`from __future__ import annotations`** - might change evaluation behavior
4. **Walrus operator in class body** - might have special evaluation
5. **`type.__subclasses__()`** through some indirect mechanism
6. **`__init_subclass__`** if it can be accessed without `_` prefix
7. **Generator/iterator protocol** - `__next__` starts with `_` so blocked

## Tool Versions
- RestrictedPython: 8.4 (latest at time of CTF)
- Python: 3.10
- CVE-2023-37271: Patched (gi_frame in INSPECT_ATTRIBUTES)
- CVE-2025-22153: Patched (try/except* removed in v8.0)
