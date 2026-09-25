$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\the_fine_print"
$out  = "$base\files\terms_of_service.txt"

$inner = "read_the_whole_terms_before_you_agree"   # 34 chars -> flag inner
$N = $inner.Length
$total = 400

# Build a hidden path of distinct section numbers, starting at 1.
$rng = New-Object System.Random(1337)
$path = New-Object System.Collections.Generic.List[int]
$path.Add(1)
while ($path.Count -lt $N) {
    $c = $rng.Next(2, $total + 1)
    if (-not $path.Contains($c)) { $path.Add($c) }
}

$filler = @(
 "The user grants ACME an irrevocable, perpetual, worldwide license to all data submitted.",
 "ACME may, at its sole discretion, monetize your attention without notice.",
 "Downtime is a feature, not a defect, and is excluded from any SLA.",
 "Support responses may take between 3 and 900 business days to arrive.",
 "All timestamps are approximate and also, technically, incorrect.",
 "The free tier is free in the same way a rock is a boat: technically present.",
 "We reserve the right to rename things without informing you.",
 "Cookies are stored, consumed, and stored again for quality assurance.",
 "Your password was observed. We mean that neutrally.",
 "By subsection 4.2.1(b) the moon is, on Tuesdays, technically ours."
)

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("=== ACME CORP TERMS OF SERVICE (Revised 2026-07-09) ===")
$lines.Add("")
$lines.Add("CORPORATE COMPLIANCE NOTICE: Your flag begins at SECTION 1.")
$lines.Add("Follow the embedded reading instructions exactly. Each instructed")
$lines.Add("section contributes one character. Stop when a section says it is the END.")
$lines.Add("")

$letterAt = @{}   # section -> letter
$nextAt   = @{}   # section -> next section (or 'END')
for ($k = 0; $k -lt $N; $k++) {
    $letterAt[$path[$k]] = $inner[$k]
    if ($k -lt $N - 1) { $nextAt[$path[$k]] = $path[$k+1] } else { $nextAt[$path[$k]] = "END" }
}

for ($s = 1; $s -le $total; $s++) {
    $lines.Add("SECTION $s.")
    if ($letterAt.ContainsKey($s)) {
        $lines.Add("  READING CHECKPOINT: the character contributed by this section is '$($letterAt[$s])'.")
        if ($nextAt[$s] -eq "END") {
            $lines.Add("  This is the END of the document. You may stop reading now.")
        } else {
            $lines.Add("  PROCEED TO SECTION $($nextAt[$s]) to continue.")
        }
    } else {
        $lines.Add("  " + $filler[($s) % $filler.Length])
        $lines.Add("  Additional subclause: the processing fee for section $s is calculated using a formula we will not disclose.")
    }
    $lines.Add("")
}

[System.IO.File]::WriteAllLines($out, $lines.ToArray())

# Compute the flag the same way a solver would, to store in flag.txt
$sb = New-Object System.Text.StringBuilder
for ($k = 0; $k -lt $N; $k++) { $null = $sb.Append($inner[$k]) }
$flag = "flag{" + $sb.ToString() + "}"
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "inner len=$N pathStart=$($path[0]) pathEnd=$($path[$N-1])"
Write-Output "flag=$flag"
