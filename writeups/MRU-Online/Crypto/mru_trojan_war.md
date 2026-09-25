# mruonline - The Trojan War (AES-128-CBC + RSA + ROT13)

## Challenge
- **CTF**: mruonline
- **Category**: crypto
- **Challenge**: The Trojan War
- **Files**: `AES.py`, `rsa.py`, `The Odyssey/Flag.txt`

## Part 1: AES-128-CBC

Ciphertext hex (96 bytes), key=`odysseus_journey`, IV=`Princess\0...`

```python
cipher = AES.new(b"odysseus_journey", AES.MODE_CBC, b"Princess".ljust(16, b"\0"))
pt = unpad(cipher.decrypt(bytes.fromhex(cipher_hex)), 16)
```

Decrypts to a Google Drive link containing `The Odyssey.zip`.

## Part 2: RSA Fermat Factorization

n (1024-bit) has p,q close together → Fermat's method:

```python
a = isqrt(n)
while True:
    b2 = a*a - n
    b = isqrt(b2)
    if b*b == b2:
        p, q = a+b, a-b
        break
    a += 1
```

Decrypts to `Princess` (confirms the AES IV).

## Part 3: ROT13

`Flag.txt` contains: `OCPGS{U3y3a_15_E3ge13i3q!!!}`

ROT13 → `BPCTF{H3l3n_15_R3tr13v3d!!!}`

## Flag
`bpctf{H3l3n_15_R3tr13v3d!!!}`
