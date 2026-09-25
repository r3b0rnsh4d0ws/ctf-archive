# STARPWN 2026 — Follow the leak (Forensics, 494pts)

## Challenge
Meridian breach investigation — point of entry originated from information inside the archive. Help recover the hidden key. Flag format STARPWN{...}.

## Files
- opensatkit-badpush-student.zip (640MB) → `student/` OpenSatKit repo (cFS + COSMOS + 42 simulator) with full `.git/`

## Recon
- Extracted archive; `student/.git` present → classic git forensics.
- `git log --all` shows story commits on top of upstream OpenSatKit history:
  - `6d7902d5` remove large binaries (HEAD)
  - `035b9b27` docs: incident report for credential scrub (history rewrite) ← self-incriminating
  - `8b64cc72` docs: add telemetry quicklook cheat sheet
  - `260db5f9` cosmos:temp lab key ← the BAD PUSH
  - `145ef834` mission and comms plan
- Reflog shows clone from `/home/quietd/badpush-ctf/origin.git/`, resets to origin/main, then commit 6d7902d5.
- packed-refs: refs/heads/main = 8ae9b83f, refs/original/HEAD = e92021ca (rewritten-history remnants).

## Analysis
- `git show 260db5f9` → added `cosmos/.cdskeyfile`:
  ```
  # NOTE: TEMPORARY — remove before flight
  CDS_KEY=ZmxhZ3s1MHJyeV9XMTVoX1czX0MwdWxkX0cwXzcwXzdoM19NMDBuXzcwZzM3aDNyfQ==
  ```
- `docs/INCIDENT.md` (added 035b9b27): admits a COSMOS credential was accidentally committed, claims history rewritten to scrub it, notes "your local Git reflog may still contain the old reference" — direct pointer to the leaked key being recoverable.
- `cosmos/.reservedkeyfile` and `cosmos/.resetkeyfile` are empty blobs (red herrings). Working tree still contains `cosmos/.cdskeyfile` with the same key.

## Exploit
```bash
echo "ZmxhZ3s1MHJyeV9XMTVoX1czX0MwdWxkX0cwXzcwXzdoM19NMDBuXzcwZzM3aDNyfQ==" | base64 -d
# → flag{50rry_W15h_W3_C0uld_G0_70_7h3_M00n_70g37h3r}
```

## Flag
`STARPWN{50rry_W15h_W3_C0uld_G0_70_7h3_M00n_70g37h3r}`

## Writeup
The "leak" is a COSMOS command/telemetry CDS key file (`cosmos/.cdskeyfile`) pushed in commit `260db5f9` "cosmos:temp lab key". The follow-up incident-report commit documents the "scrub" but history was never actually purged — reflog + packed-refs still reference the pre-rewrite state, and the key commit is plainly visible in `git log --all`. Decoding the base64 CDS_KEY yields the flag. Key insight: the "history rewrite" story is the anti-AI decoy — the secret is still in plain sight in commit history.

## Lessons
- Always run `git log --all`, `git reflog`, `git fsck --lost-found` on CTF git dumps; a "credential scrub" incident doc is an admission, not a fix.
- Base64 blobs in config/key files decode directly; grep for `KEY=`/`keyfile`/`secret`/`cred` filenames in history.
- Empty placeholder keyfiles are red herrings — check contents.
