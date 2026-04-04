$dir = 'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation\'
$files = Get-ChildItem "$dir*.html"

foreach ($f in $files) {
  $content = [System.IO.File]::ReadAllText($f.FullName)

  # The footer "Legal Recognition" link was accidentally changed to /privacy-policy
  # Restore it to legal-recognition.html
  if ($content -match 'href="/privacy-policy">Legal Recognition') {
    $content = $content.Replace('href="/privacy-policy">Legal Recognition', 'href="legal-recognition.html">Legal Recognition')
    [System.IO.File]::WriteAllText($f.FullName, $content, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED: $($f.Name)"
  } else {
    Write-Host "OK: $($f.Name)"
  }
}
Write-Host "Done."
