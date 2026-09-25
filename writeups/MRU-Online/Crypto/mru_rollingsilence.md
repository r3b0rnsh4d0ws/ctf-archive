# mruonline - rollingsilence (Rolling XOR Cipher)

## Challenge
- **CTF**: mruonline
- **Category**: crypto / rev
- **Challenge**: rollingsilence
- **File**: `rollingsilence` (stripped ELF 64-bit binary)

## Method

Reverse-engineer the binary entry point. The `.rodata` section contains 26 encoded bytes. The decoder loop:

1. XOR byte with key (init=0x89)
2. key = (key + i) & 0xFF
3. key = ROL(key, 1)
4. key ^= 0xA5

```python
data = bytes.fromhex("ebc6a948bd61e98319c1b570de58b8498e2816f155a5092d2062")
key = 0x89
out = []
for i, b in enumerate(data):
    out.append(b ^ key)
    key = (key + i) & 0xff
    key = ((key << 1) & 0xff) | (key >> 7)
    key ^= 0xA5
print(bytes(out).decode())
```

## Flag
`bpctf{registers_are_state}`
