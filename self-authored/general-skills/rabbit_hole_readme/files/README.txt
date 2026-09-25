We encrypted the flag. To recover it you must apply the exact sequence of
transformations below, in order, to the seed value. Deviate and you get garbage.
There is only one correct path.

SEED (apply the steps to this string):
General Skills Time Cube 2026

STEPS (in order):
1. ROT13 the entire string.
2. Base64-encode the result (UTF-8).
3. Reverse the string.
4. Caesar shift the string by +5 (alphabetic characters only; preserve case and non-letters).
5. Base64-encode the result again (UTF-8).
6. Keep ONLY the characters at ODD indices (1, 3, 5, ...; 0-based).
7. Wrap the final result in flag{...}.

Download: README.txt