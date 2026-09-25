# BushBash - Hack The Vault II (Pwn, Easy)

## Flag
`bushbash{1nto-th3-bUsh-w3-Go}`

## Challenge
Sequel to Hack The Vault I. `nc 34.40.133.67 7778`, source `vault.c` given. Author: Harold Gao.

## Solution
- Source: `char array[127+64]`, `buffer=&array[0]`, `password=&array[127]` (adjacent)
- Sending exactly 127 chars makes `buffer[127]='\0'` land on `password[0]`, but
  `fread(password,...)` immediately restores it
- `printf("password you entered: %s\n", buffer)` then has **no NUL inside our
  input** (NUL went at offset 127 = password) → `%s` prints past input into
  `password.txt` → OOB stack leak
- **Exploit**: send `'A'*127+'\n'` → parse the leaked password
  `GNk1f:sH)7#uY9$1vpS5c~Z^I#&fe6*a` → send it + `\n` → flag
- Password length probed first (26 leaked chars; actual file content 32 bytes)

## Authoring Notes
- Sequel in the Moss Man/Kane saga; success message teases another chapter
- Author ships source → this is a pure logic/off-by-one puzzle, no binary RE
- The "input exceeded buffer limit" guard bounds writes but NOT the NUL write —
  that off-by-one NUL is the entire vulnerability (enables the `%s` OOB leak)
- `fread` after the NUL write is the crux: leak fires AND auth still works

## Lessons
- Whenever a program echoes your input (`%s`/puts/printf), check if the input is
  NUL-terminated inside its own buffer and what sits adjacent after it
- Off-by-one NUL overwrites aren't only for canary clobbering — a NUL landing at
  the start of an adjacent secret buffer + `%s` = free secret leak
- Trace data flow after the guard (the post-guard `fread` decides exploitability)
- Remote buffer-size mapping via "exceeded limit" messages (127 vs 128)
