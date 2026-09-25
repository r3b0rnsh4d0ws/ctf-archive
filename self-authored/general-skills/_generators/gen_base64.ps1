$ErrorActionPreference = "Stop"
$base = "C:\Users\balu\ctf-general-challenges\recursive_base64"
$out  = "$base\files\data.b64"

$flag = "flag{its_base64_all_the_way_down}"
$bytes = [Text.Encoding]::UTF8.GetBytes($flag)
$layers = 30
for ($i = 0; $i -lt $layers; $i++) {
    $encoded = [Convert]::ToBase64String($bytes)
    $bytes = [Text.Encoding]::UTF8.GetBytes($encoded)
}

# No literal flag, no comments: just the final base64 blob.
[System.IO.File]::WriteAllText($out, $encoded)

# sanity: decode back
$verify = $bytes
for ($i = 0; $i -lt $layers; $i++) {
    $s = [Text.Encoding]::UTF8.GetString($verify)
    $verify = [Convert]::FromBase64String($s)
}
Set-Content -Path "$base\flag.txt" -Value $flag -NoNewline
Write-Output "layers=$layers bloblen=$($encoded.Length) verify=$([Text.Encoding]::UTF8.GetString($verify))"
