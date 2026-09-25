# BushBash - Password (Misc, 100pts Easy)

## Flag
`bushbash{i_l0v3_C0bs}`

## Challenge
"We've recovered a device with a usb port. We know the username is admin and the password is password, but we just can't log in. The info we received was a cobbled mess, maybe something's missing?" — `nc 34.40.133.67 6768`. Author: Eisverygoodletter.

## Solution
The service speaks a COBS-style length-prefixed protocol: every message is `[length byte][payload\x00]` (server and client BOTH frame). Sending raw strings fails with:
- `Error occured during decoding`
- `not enough input bytes for length code` ← the tell: first byte is parsed as a length

Login with framed credentials:
1. `b'\x06' + b'admin\x00'` → `Waiting for password...`
2. `b'\x09' + b'password\x00'` → `Your flag is bushbash{i_l0v3_C0bs}`

Username/password were literally admin/password — the puzzle was the framing. "Cobbled mess" = COBS wordplay.

## Authoring Notes
- Wrapped a trivial login in a `[len][str\x00]` framing layer on BOTH directions
- Deliberate misleading errors ("decoding error") to send solvers down HID/encoding rabbit holes
- USB theme is pure flavor; challenge is protocol-framing awareness
- Easy difficulty: creds given, only framing needs discovery

## Lessons
- "not enough input bytes for length code" ⇒ input must be `[len][payload]`, never raw
- Mirror the server's framing for your own messages
- Payload length includes the `\x00` terminator: `len = len(str) + 1`
- Error messages are protocol oracles — read them before theorizing about HID/crypto
