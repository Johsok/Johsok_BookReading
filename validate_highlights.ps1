$files = @(
  'Books/04_healthcare/04_healthcare-20260717-54.json',
  'Books/04_healthcare/04_healthcare-20260717-55.json'
)
$sep = [char]0x3001
foreach ($f in $files) {
  $j = Get-Content $f -Raw -Encoding UTF8 | ConvertFrom-Json
  $h = $j.chatgptHighlights
  $bad = 0
  for ($i = 0; $i -lt $h.Count; $i++) {
    $prefix = ('{0:D3}' -f ($i + 1)) + $sep
    if (-not $h[$i].StartsWith($prefix)) { $bad++ }
  }
  Write-Output ("{0} | count={1} | source={2} | status={3} | at={4} | badNumbering={5}" -f $f, $h.Count, $j.highlightsSource, $j.chatgptStatus, $j.highlightsCapturedAt, $bad)
}
