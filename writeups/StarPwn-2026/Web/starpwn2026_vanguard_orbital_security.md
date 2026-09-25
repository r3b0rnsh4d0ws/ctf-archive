# Vanguard Orbital Security — STARPWN 2026 (Ground Operations)

## Summary
Obtained a shell on an air-gapped CI/CD host via a custom ttyd terminal endpoint, then read the container's `FLAG` env var (which is the value of the `PROD_SIGNING_KEY` Gitea Actions secret the challenge asks for).

**Flag:** `STARPWN{k1ck_1091c_70_7h3_cu28_4nd_d0_7h3_1mp0551813}`

## Target
- Gitea 1.23.8 (public) + ttyd terminal at `https://<host>/shell/`
- Internal Gitea at `127.0.0.1:3000`, air-gapped from public net; shell is the bridge

## Steps
1. **Recon:** `/shell/` serves a ttyd client page (vshell.html). `/shell/token` returns `{"token": ""}` (auth disabled).
2. **Protocol RE from the client bundle** (vshell.html constants):
   - WS endpoint: `wss://<host>/shell/ws` with subprotocol `tty`
   - Client→Server frames: first byte ASCII `"0"` (0x30) = INPUT + UTF-8 data (ttyd binary protocol)
   - Server→Client: `"0"`=output, `"1"`=window title, `"2"`=preferences
3. **Handshake gotcha:** the server requires an initial JSON frame `{"AuthToken":"","columns":100,"rows":40}` before any input; sending input first drops the connection (1006).
4. **Shell:** `id` → `uid=1001(player)`; `env | sort` → `FLAG=STARPWN{...}` right in the terminal environment.
5. **Verification:** read `/setup/seed-gitea.sh` — it sets repo secret `PROD_SIGNING_KEY: $FLAG` on `challenges/build-service`. Confirmed the env FLAG == the secret's value. No other STARPWN flags anywhere on disk.

## Intended path (not needed — env leak)
- `player` shell → `/home/player/backup.env` gives `builddev:devsync_9f3a_build` (write access to the private repo granted via API in seed-gitea.sh)
- Push a malicious `.gitea/workflows/release.yml` to `challenges/build-service` → host runner (`/data/runner/.runner`, labels `ubuntu-latest:host`) executes job → `env: SIGNING_KEY: ${{ secrets.PROD_SIGNING_KEY }}` → exfiltrate = flag.

## Technique: ttyd custom-protocol shell
1. `GET /shell/token` → JSON token (may be empty = auth off)
2. `wss://<host>/shell/ws` subprotocol `tty`
3. Send `{"AuthToken":"<token>","columns":80,"rows":24}` as FIRST frame
4. Send `b"0" + cmd.encode() + b"\r"` for each command (ASCII '0' type byte)
5. Strip ANSI from output (regex `\x1b\[[0-9;?]*[a-zA-Z]`)
