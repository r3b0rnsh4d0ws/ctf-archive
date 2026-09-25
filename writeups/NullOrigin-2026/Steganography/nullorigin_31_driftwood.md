# NullOrigin Stego Chain — 31-driftwood

## Challenge
| | |
|---|---|
| CTF | NullOrigin (stego chain) |
| Stage | 31-driftwood (1 of 8) |
| Category | Steganography |
| Files | `driftwood.png`, `plate-card.txt` |
| Flag format | `Null0rigin{lowercase_words_with_underscores}` |

## Files
- `driftwood.png` — 900x620 8-bit RGBA PNG (534120 bytes)
- `plate-card.txt` — keeper's index card describing the "works entry" framing format
- `description.txt` — empty

## Recon
The chain README: 8 stages (31-driftwood → 38-quietus), each stage's flag is the key to the next. No verify binary; wrong key gives no signal. Keep untouched copies (SHA256SUMS).

The plate-card is the instruction sheet for this room. It defines the **works entry** format used by the plate room:

```
PL8     works stamp, three characters
.       one character, the issue of the stamp
..      the length of the entry, two characters, low first
....    a check over the entry, four characters, low first
....    the entry itself
```

The check is "the ordinary one" — CRC32. The keeper warns: if extracted data does not begin with the stamp and the check does not validate, it is "somebody's handwriting" (a decoy), and "some of it was left to be found."

## Analysis
zsteg triage surfaced three candidate payloads:

1. **393 bytes appended after IEND** — a ZIP containing `single.txt` and `sleeve4/.keep`. Decoy.
2. **PNG meta Comment**: `recovered from the shingle, sleeve 4 - NullOrigin{the_tide_returns_what_it_took}`. Decoy — wrong flag format (capital O in Origin) and no works stamp.
3. **Red channel LSB (row-major)**: `Null0rigin{pit_head_plate_number_four}`. Matches flag format but has **no PL8 stamp** → per the keeper, this is handwriting. Decoy.

The real payload must be a valid works entry. Brute-forced every channel (R/G/B/A), bit plane (1-8), bit order (LSB/MSB), and scan direction (xy/yx) for the `PL8` magic using numpy packbits:

**Hit: alpha channel, bit 0 (LSB), column-major (yx)** — the stream begins exactly with the works entry:

```
50 4c 38 01 3a 00 eb c2 a0 ba 4e 75 6c 6c 30 72 ...
P  L  8  .  :  .  .  .  .  .  N  u  l  l  0  r  ...
```

## Exploit
Parse the works entry:

| Field | Bytes | Value |
|---|---|---|
| Stamp | `PL8` | works stamp |
| Issue | `01` | issue 1 |
| Length | `3A 00` | 0x003A = 58 (low first) |
| Check | `EB C2 A0 BA` | 0xBAA0C2EB (low first) |
| Entry | 58 bytes | flag + 9 trailing bytes |

Verify the check: `CRC32(entry) = 0xBAA0C2EB` — **exact match**. The entry is a genuine works entry.

Entry content:
```
Null0rigin{what_the_negative_kept_from_the_print} 1f 9e 4c 1a f0 d3 b2 76 51
```

The 9 trailing bytes after the closing brace are padding/forward hint — the flag text itself points at stage 32-safelight ("what the negative kept from the print" → `negative.png` / `print.png`).

## Flag
```
Null0rigin{what_the_negative_kept_from_the_print}
```

## Writeup / Lessons
- **Framed payload format**: `STAMP(3) + ISSUE(1) + LEN(2 LE) + CRC32(4 LE) + DATA` is a self-validating container. The stamp + CRC32 gate separates real data from decoys — trust the frame, not the readable text.
- **Column-major LSB**: the payload was hidden in the alpha channel LSB read **column-by-column** (yx), which zsteg's default `xy` scans miss. Always brute-force channel × plane × order × direction.
- **Decoy discipline**: metadata comments and obvious LSB planes carried plausible-looking flags. The keeper's note was the key to knowing they were fake — read the flavor/documentation before trusting extracted strings.
- **CRC32 as "the ordinary check"**: 4-byte little-endian check over the entry = CRC32. Any clerk (zlib) can run it.

## Authoring notes (how this was built)
- Carrier: RGBA PNG; payload in alpha channel LSB, column-major order.
- Frame: `PL8` + issue byte + uint16 LE length + uint32 LE CRC32 + payload.
- Decoys: PNG tEXt Comment with a near-flag, red-channel LSB with a format-valid flag, appended ZIP with a text file — all without the stamp/check so they fail the keeper's test.
- Chain design: flag text hints the next stage's theme (negative/print → safelight).