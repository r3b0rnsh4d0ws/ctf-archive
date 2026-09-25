$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\tiny_text_svg"
$out  = "$base\files\poster.svg"
$flag = "flag{zoom_and_enhance_like_a_spy_movie}"

# ROT13 (letters only)
$rot = ''
foreach ($c in $flag.ToCharArray()) {
    if ($c -cmatch '[a-z]') { $rot += [char](([int]$c - 97 + 13) % 26 + 97) }
    elseif ($c -cmatch '[A-Z]') { $rot += [char](([int]$c - 65 + 13) % 26 + 65) }
    else { $rot += $c }
}

$svg = @"
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="220" viewBox="0 0 800 220">
  <rect width="800" height="220" fill="#0d1117"/>
  <text x="20" y="60" font-family="monospace" font-size="24" fill="#39d353">Congratulations, you can see. But can you READ what you see?</text>
  <text x="20" y="110" font-family="monospace" font-size="14" fill="#8b949e">Some text is printed so small it is invisible at normal zoom.</text>
  <text x="10" y="130" font-family="monospace" font-size="0.01" fill="#39d353">$rot</text>
  <text x="20" y="180" font-family="monospace" font-size="14" fill="#8b949e">hint: the tiny text above is encoded with a classic 13-shift cipher.</text>
</svg>
"@
[System.IO.File]::WriteAllText($out, $svg)
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "rot13=$rot"
