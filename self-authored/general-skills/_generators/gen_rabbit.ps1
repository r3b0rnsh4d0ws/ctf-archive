$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\rabbit_hole_readme"

function RotN($s, $n) {
    $out = ''
    foreach ($c in $s.ToCharArray()) {
        if ($c -match '[a-zA-Z]') {
            $base = if ($c -cmatch '[a-z]') { 97 } else { 65 }
            $out += [char](([int]$c - $base + $n) % 26 + $base)
        } else { $out += $c }
    }
    return $out
}
function B64($s) { return [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($s)) }
function Rev($s) { return -join ($s.ToCharArray() | ForEach-Object { $_ } | Sort-Object -Descending { $true } ) }
# proper reverse:
function Reverse($s) { $a = $s.ToCharArray(); [Array]::Reverse($a); return -join $a }

$seed = "General Skills Time Cube 2026"

# Step 1: ROT13
$a = RotN $seed 13
# Step 2: base64
$b = B64 $a
# Step 3: reverse
$c = Reverse $b
# Step 4: Caesar +5 (letters only)
$d = RotN $c 5
# Step 5: base64 again
$e = B64 $d
# Step 6: keep only characters at ODD indices (1,3,5,...)
$f = ''
for ($i = 1; $i -lt $e.Length; $i += 2) { $f += $e[$i] }
$flag = "flag{$f}"

$readme = @"
We encrypted the flag. To recover it you must apply the exact sequence of
transformations below, in order, to the seed value. Deviate and you get garbage.
There is only one correct path.

SEED (apply the steps to this string):
$seed

STEPS (in order):
1. ROT13 the entire string.
2. Base64-encode the result (UTF-8).
3. Reverse the string.
4. Caesar shift the string by +5 (alphabetic characters only; preserve case and non-letters).
5. Base64-encode the result again (UTF-8).
6. Keep ONLY the characters at ODD indices (1, 3, 5, ...; 0-based).
7. Wrap the final result in flag{...}.

Download: README.txt
"@
Set-Content -Path "$base\files\README.txt" -Value $readme -NoNewline
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "flag=$flag"
