$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\needle_in_haystack"
$out  = "$base\files\access.log"
$flag = "flag{grep_is_faster_than_reading}"
$bytes = [Text.Encoding]::UTF8.GetBytes($flag)
$N = $bytes.Length
$total = 300000

$rng = New-Object System.Random(2026)
$ips = @("10.0.0.1","192.168.1.5","172.16.3.9","203.0.113.7","8.8.8.8","198.51.100.23")
$paths = @("/index.html","/login","/api/v1/users","/static/app.js","/favicon.ico","/admin","/robots.txt")
$agents = @("Mozilla/5.0","curl/7.68","python-requests/2.25","Go-http-client","Bingbot/2.0")

# Build injection map: real flag bytes at /internal/ with status 418, in order.
$step = [math]::Floor($total / ($N + 1))
$inject = @{}   # lineNumber -> text
for ($k = 0; $k -lt $N; $k++) {
    $ln = [int](($k + 1) * $step)
    $hex = $bytes[$k].ToString("x2")
    $inject[$ln] = "203.0.113.7 - - [09/Jul/2026:22:00:00 +0000] `"GET /internal/metrics?b=$hex HTTP/1.1`" 418 0 `"-`" `"Mozilla/5.0`""
}
# Decoy 418 lines (status 418 but path NOT /internal/) with random hex noise.
$decoys = 2500
for ($d = 0; $d -lt $decoys; $d++) {
    $ln = $rng.Next(1, $total)
    $noise = ($rng.Next(0, 65536)).ToString("x4")
    $p = $paths[$rng.Next($paths.Length)]
    if (-not $inject.ContainsKey($ln)) {
        $inject[$ln] = "10.0.0.1 - - [09/Jul/2026:22:00:00 +0000] `"GET $p?token=$noise HTTP/1.1`" 418 0 `"-`" `"curl/7.68`""
    }
}

$keys = [int[]]@($inject.Keys) | Sort-Object
$fw = [System.IO.StreamWriter]::new($out, $false)
$ptr = 0
for ($i = 1; $i -le $total; $i++) {
    if ($ptr -lt $keys.Length -and $i -eq $keys[$ptr]) {
        $fw.WriteLine($inject[$keys[$ptr]])
        $ptr++
    } else {
        $ip = $ips[$rng.Next($ips.Length)]
        $p = $paths[$rng.Next($paths.Length)]
        $a = $agents[$rng.Next($agents.Length)]
        $st = @(200,200,200,301,404)[$rng.Next(5)]
        $fw.WriteLine("$ip - - [09/Jul/2026:22:00:00 +0000] `"GET $p HTTP/1.1`" $st $($rng.Next(50,9999)) `"-`" `"$a`"")
    }
}
$fw.Close()
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "total=$total flagBytes=$N injectedInternal=$(($inject.Keys | Where-Object { $inject[$_] -match '/internal/' }).Count) decoys=$(($inject.Keys | Where-Object { $inject[$_] -notmatch '/internal/' }).Count)"
