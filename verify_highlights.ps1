$files = @(
  'Books/04_healthcare/04_healthcare-20260717-48.json',
  'Books/04_healthcare/04_healthcare-20260717-49.json'
)
$sep = [char]0x3001
foreach ($f in $files) {
  $j = Get-Content $f -Raw -Encoding UTF8 | ConvertFrom-Json
  $h = $j.chatgptHighlights
  $ok = $true
  for ($i = 0; $i -lt $h.Count; $i++) {
    $prefix = ('{0:D3}' -f ($i + 1)) + $sep
    if (-not $h[$i].StartsWith($prefix)) { $ok = $false; break }
  }
  Write-Output ($f + ' | count=' + $h.Count + ' | numbering=' + $ok + ' | source=' + $j.highlightsSource + ' | status=' + $j.chatgptStatus + ' | capturedAt=' + $j.highlightsCapturedAt)
}
