# Kali Team CTF 26 - Robots (Web, 100 pts)

## Challenge
- **CTF:** Kali Team - CTF 26 (private platform, kali-team.online)
- **Category / Points:** Web / 100
- **Solves:** 249 at solve time
- **Author:** F4R3S
- **Flag format:** `KaliTeam{...}`
- **Instance:** http://68d4.chall.kali-team.online:8001/

## Description (paraphrased)
"Our servers have evolved. They no longer see code; they see the glitch in your
biological existence. You claim to be 'superior' while your species excels only at
destruction and theft. Task: Prove your worth to the Silicon Intelligence. If you can
still find your 'humanity' in the rubble we've logged."

## Files
None — pure live web instance.

## Recon
- `GET /` returned a static propaganda page (Apache/2.4.25, static file served with
  ETag/Last-Modified). Footer hint: "SYSTEM LOG: Human conscience not found.
  Error 404: Humanity not found in the rubble."
- `GET /robots.txt` returned a PHP-generated taunt (`X-Powered-By: PHP/7.0.33`)
  addressed to "DEAR HUMAN" — mocking humans while boasting about GOOGLEBOTS.
  No Disallow directives.
- Directory fuzz of ~55 common paths (`/flag`, `/admin`, `/logs`, `/glitch`,
  `/humanity`, `/secret`, `.git`, `.env`, etc.) — all 404 except `/` (200) and
  `.htaccess` (403).
- The taunt explicitly named GOOGLEBOTS and mocked clicking "I AM NOT A ROBOT" —
  strong hint that the server behaves differently for bot User-Agents.

## Analysis
The key signal was the challenge name ("Robots") plus the robots.txt taunt pointing
at crawler user-agents. The site's robots.txt is served dynamically by PHP and its
content depends on the requesting User-Agent:

- Human User-Agent -> taunt (red herring, no flag)
- Googlebot User-Agent -> the "real" robots.txt, which contains the flag

## Exploit
```bash
curl -s -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  http://68d4.chall.kali-team.online:8001/robots.txt
```

## Flag
```
KaliTeam{900ae6c4-7b07-40b1-b7f4-5ce26af85a54}
```

## Writeup
1. Load `/` and `/robots.txt`. The robots.txt is a dynamic PHP response that taunts
   humans and praises GOOGLEBOTS.
2. The challenge is named "Robots" — the intended trick is User-Agent fingerprinting.
3. Re-request `/robots.txt` with a Googlebot User-Agent. The server switches content
   and returns the flag inside the "crawler" version of robots.txt.
4. Flag format `KaliTeam{...}` validated.

## Lessons / Technique
- **User-Agent-dependent content switching on robots.txt (and any dynamic route).**
  When a robots.txt response is dynamically generated and the challenge theme hints
  at crawlers, re-request it (and the whole site) with Googlebot / Bingbot /
  GPTBot / other crawler UAs. This is a classic "warmup" web trick.
- Red-herring propaganda text inside robots.txt is a deliberate distraction; look
  for the entity the server is "addressing" (here: GOOGLEBOTS) and impersonate it.
- Always check response headers: `X-Powered-By: PHP` on robots.txt revealed it was
  dynamic, unlike the static index page — a sign the response varies per request.

## Difficulty verdict
100 pts / 249 solves = beginner warmup. Matches expected difficulty.

## Author note (how it was built)
- Apache + PHP backend; index.html is a static file, robots.txt is a PHP script
  (probably `robots.php` or an `index.php` route) that branches on
  `$_SERVER['HTTP_USER_AGENT']` and prints either the taunt or the flag.
- Flag is hardcoded/embedded server-side, not in a file readable via LFI.
