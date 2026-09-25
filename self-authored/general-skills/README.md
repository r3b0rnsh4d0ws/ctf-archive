# General Skills — Time-Waster CTF Challenges

A set of 8 misdirection/"General Skills" challenges in the spirit of NahamCon's
love for wasting players' time. **Design rules for this set:**

- The flag is **never stored as a literal `flag{...}` string** in any
  downloadable file — a plain `grep "flag{"` finds nothing.
- Every challenge has **exactly one intended solution path** (documented in
  `solution.md`). There is no shortcut that drops the flag in your lap.
- Each challenge is a **fair grind**: the instructions are complete and the
  answer is always reachable, but players must actually do the work.

## Folder layout (CTFd-ready)
```
<challenge>/
  description.txt   # prompt shown to players
  flag.txt          # the flag (import ONLY into your CTFd instance)
  solution.md       # author writeup / intended single path
  files/            # downloadable artifacts (no literal flag inside)
```

## Importing into CTFd
1. Create a challenge (category: General / General Skills).
2. Paste `description.txt` as the description.
3. Set the flag from `flag.txt` (the `flag{...}` value).
4. Attach the contents of `files/` as the download.
5. Keep `solution.md` private.

## The challenges
| Folder             | Single intended path                                                   | Flag                                      |
|--------------------|------------------------------------------------------------------------|-------------------------------------------|
| the_fine_print     | Follow SECTION cross-reference links; collect 1 char/section, in order | flag{read_the_whole_terms_before_you_agree} |
| rabbit_hole_readme | Apply the documented 6-step transform chain to the SEED                | flag{UvmOUkUmkuDF1sEqUNkHG6XoUNQ=}        |
| whitespace_secrets | Decode trailing SPACE=0 / TAB=1 bits, 8 bits per character             | flag{whitespace_is_a_character_too}       |
| recursive_base64   | base64-decode 30 times until it becomes readable                       | flag{its_base64_all_the_way_down}         |
| git_blunder        | Inspect `git log`; a commit message is base64 of the flag             | flag{git_blunder_reveals_the_past}        |
| tiny_text_svg      | Read the 0.01px tiny text; it is ROT13 of the flag                    | flag{zoom_and_enhance_like_a_spy_movie}   |
| obfuscated_script  | Run the script; flag is reconstructed from char codes at runtime       | flag{obfuscation_is_just_security_theater}|
| needle_in_haystack | Filter `/internal/`+418 lines; concat `b` hex bytes; decode           | flag{grep_is_faster_than_reading}         |

## Difficulty notes
- **Easiest (still non-trivial):** whitespace_secrets, tiny_text_svg.
- **Medium grind:** rabbit_hole_readme, recursive_base64, obfuscated_script.
- **Longest slog:** the_fine_print (link-following), needle_in_haystack (parse
  300k lines), git_blunder (history spelunking).
