# Jersy CTF - Darkside (AES-256-CBC Decrypt)

## Challenge
- **CTF**: Jersy
- **Category**: Crypto
- **Challenge**: Darkside
- **Files**: `hash.bin`, `hash.txt`, `intercepted.txt`

## Given
- AES-256-CBC ciphertext (hex, 2464 chars = 1232 bytes)
- Secret Key: `ecf2584110823e9d31c049207f8034b923f213b52c1ea9a2a18661dc6063a400`
- IV: `91e94784686346258e6acc81009edd65`

## Solution
1. Parse `intercepted.txt` to extract key, IV, and ciphertext
2. Decrypt using PyCryptodome AES-CBC
3. Remove PKCS7 padding
4. Extract base64-encoded NV_MEM_DUMP from decrypted log: `amN0ZntyZWxheV9zYWZlX21vZGVfYWN0aXZhdGVkXzIwMjZ9`
5. Base64 decode → flag

```python
from Crypto.Cipher import AES
key = bytes.fromhex("ecf2584110823e9d31c049207f8034b923f213b52c1ea9a2a18661dc6063a400")
iv = bytes.fromhex("91e94784686346258e6acc81009edd65")
ct = bytes.fromhex(ciphertext_hex)
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)
pt = pt[:-pt[-1]]  # remove PKCS7 padding
print(pt.decode())
```

## Flag
`jctf{relay_safe_mode_activated_2026}`

## Technique
AES-256-CBC decryption with known key and IV. Key/IV leaked in intercepted file.
