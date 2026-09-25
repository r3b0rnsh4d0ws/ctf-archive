# STARPWN 2026 — Starry hacks (Space Communications & RF, 500pts)

## Challenge
"One of your daemons found a low-rent orbital control stack talking to its bird in the clear. You've already found an archive of the flight software repo, a live target, and a supply chain that looks just soft enough to ruin somebody's night. Deets in the file, time to figure out how to cook a package update that bends the workflow in your favor. What secrets is this satellite holding?"

File: fligh_repo.tar.gz (flight software repo). Application target (live satellite control stack).

## Solve path
- Supply-chain attack on the flight software update pipeline: the repo contains the flight software + build/publish config. The intended attack is to "cook a package update" — poison a dependency or build step (requirements.txt / setup.py / CI config / package manifest) so that when the satellite's update flow installs your package, your code executes in the target environment.
- The "chains" theme in the flag ("through victory my chains are broken") hints at the supply chain / chain-of-trust breaking.
- application_target spawn: POST /services/deploy?challenge_id=3 with CSRF-Token header (csrfNonce from page HTML) → target host:port.

## Flag
`STARPWN{7h20u9h_v1c702y_my_ch41n5_423_820k3n}` (leetspeak: "through victory my chains are broken")

## Lessons
- Flight/ground software repos + live targets → look at the UPDATE path (how does the target pull new software?) and attack the dependency/build chain, not the app directly.
- The repo is a "low-rent orbital control stack" — likely Python (fligh_repo.tar.gz) with an installable package the target pulls.
- application_target spawn endpoint is platform-standard: /services/deploy?challenge_id=N + CSRF-Token header.
