# AmateursCTF 2024 — one_shot

**Category**: Web | **Difficulty**: Medium | **Status**: SOLVED

## Challenge
Flask + SQLite app. Each session creates a table `table_<16-hex-id>` containing one row: a random 32-hex password and a `searched` flag ("you have one shot"). You can search once (`LIKE` on the password) and guess once. Correct guess → flag; wrong guess → table dropped. Search results only show the **first character** of each matching row.

## Vulnerability
**SQL injection** in the `query` parameter (raw f-string interpolation inside `LIKE '%{query}%'`). The "one shot" limit doesn't stop data exfiltration because a single injected query can return the whole password.

## Exploit (one search, then guess)

The search query becomes:
```sql
SELECT password FROM table_<id> WHERE password LIKE '%<inject>%'
```

Payload — a `UNION ALL` chain that returns the password shifted by one char per row, so each row's *first* char (the only char displayed) is one character of the password:
```
' AND 0 UNION ALL SELECT substr(password,1,32) FROM table_<id>
         UNION ALL SELECT substr(password,2,32) FROM table_<id>
         ... UNION ALL SELECT substr(password,32,32) FROM table_<id> --
```

Each row `substr(password,k,32)` displays `password[k-1]` + `*`s → parse the 32 `<li>X*****</li>` entries in order, concatenate the first chars, POST it to `/guess`, get the flag.

## Critical gotcha (the real lesson)
**SQLite `UNION` sorts and deduplicates result rows** — the 32 rows come back in shuffled order and the recovered "password" is garbage (first exploit attempt failed). **`UNION ALL` preserves row order** and is mandatory when positional row order carries information.

## Flag
`L3AK{one_shot_test_flag_locally_ok}` (local test; original remote flag at one-shot.amt.rs)

## Solution script
`exploit.py` in this folder. Steps: `POST /new_session` → parse id → `POST /search` with union payload → regex `<li>(.)` over response → `POST /guess` with recovered password.
