# L3akCTF 2026 — L3ak APT (Forensics, 114 pts)

**Flag:** `L3AK{For3nsics_hUm4n$_C4n_c00K_AI}`

## Challenge
A hacker bragged on a dark web forum about possessing "super secret data" and claimed
to have joined an APT. We have a forensic copy of his system — prove he's a fraud.

## Files
`L3AK_APT.zip` (138 MB, 1467 entries) — KAPE-style Windows triage of user "Max":
- `C\$MFT`, `C\$LogFile`, `C\$Extend\$J` (USN journal), `$Secure_$SDS`
- `C\Windows\System32\winevt\Logs\` (Sysmon.evtx 16.8 MB, Security.evtx)
- Full `C\Users\Max\` profile: NTUSER.DAT, uTorrent, Discord (Cache_Data + leveldb),
  Recent .lnk, Explorer thumbcache_*.db
- `Windows.edb` (search index), Amcache.hve, Prefetch, SRUM

## Recon
1. **uTorrent** — `resume.dat` (bencode) showed `important files.7z` downloaded to
   `C:\Users\Max\Downloads\important files.7z` (added 2026-06-07 21:21:56 UTC, done in 17 s).
   `important files.torrent`: single file `important files.7z` (7,168,714 B),
   tracker `udp://tracker.opentrackr.org:1337/announce`, created by qBittorrent v5.2.3
   (`created_torrent=0` → he did NOT make it — got it from the "dark web forum").
2. **Recent .lnk files** (pylnk3) revealed the layout:
   - `Downloads\important files\Projects\media\ARS-SEC-154.png`
   - `Downloads\important files\Projects\media\ARS-CB-047.png`
   - `Downloads\discord.zip`, `ben.torrent`, `wordtemplate.torrent`, `test.txt`
   - USB drive E:\ ("New folder (2)") — phone-like content
3. **Explorer thumbcache_1280.db** etc. — 720x1280/852x1280 JPEGs → phone-screenshot proportions.

## Analysis
- Discord leveldb is encrypted (safeStorage) — dead end for message content; the
  Cache_Data `f_*` files held cached images but were not the primary payload.
- The real content lived in **Explorer thumbnails**: carved JPEG/PNG blobs from
  `thumbcache_1280.db`, `thumbcache_768.db`, `thumbcache_256.db` (scan for
  `FF D8 FF` / `89 50 4E 47`).

## Exploit / Find
The thumbnails are all **AI-generated fan art / memes**, not intelligence:
- "RIZZLER" cyberpunk character — pink text at the bottom reads:
  **`L3AK{For3nsics_hUm4n$_C4n_c00K_AI}`**
- "Mantis Blade V3.2" spec sheet (Arasaka), "Soulkiller 2.0" poster (Cyberpunk 2077)
- Ben 10 game screenshot, "SKILL ISSUE" memes, synthwave wallpapers

## Flag
`L3AK{For3nsics_hUm4n$_C4n_c00K_AI}` — "Forensics humans can cook AI":
the "super secret data" was AI-generated fan art passed off as stolen APT intel.

## Lessons
1. **Thumbcache is a content source when payload files are absent** — Explorer caches
   thumbnails of every image the user actually viewed; carve `FFD8FF`/`PNG` signatures
   directly out of `thumbcache_1280.db` (also 768/256/96/32).
2. **Bencode artifacts**: uTorrent `resume.dat` gives download paths + timestamps;
   `created_torrent` flag distinguishes torrents the user made vs. downloaded.
3. **Discord leveldb** (local storage) is encrypted with app safeStorage → parse the
   **Cache_Data** instead for plaintext cached attachments.
4. **Screenshot proportions** (720x1280) hint the source (phone) — helps read the story.
5. Recent `.lnk` files reconstruct folder structure of data that was never collected.
