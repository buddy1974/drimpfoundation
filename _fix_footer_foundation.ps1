$dir = 'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation\'
$files = Get-ChildItem "$dir*.html"

# The footer Foundation section incorrectly has href="/privacy-policy">Legal</a>
# (for files that originally had short link text "Legal" instead of "Legal Recognition")
# Restore it to legal-recognition.html, but only within the Foundation ul block
# (between about.html and executive-bureau.html)

$wrongPattern = '<li><a href="about.html">About</a></li>
            <li><a href="/privacy-policy">Legal</a></li>
            <li><a href="executive-bureau.html">Executive Bureau</a></li>'

$fixedPattern = '<li><a href="about.html">About</a></li>
            <li><a href="legal-recognition.html">Legal</a></li>
            <li><a href="executive-bureau.html">Executive Bureau</a></li>'

foreach ($f in $files) {
  $content = [System.IO.File]::ReadAllText($f.FullName)

  if ($content -match [regex]::Escape($wrongPattern)) {
    $content = $content.Replace($wrongPattern, $fixedPattern)
    [System.IO.File]::WriteAllText($f.FullName, $content, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED footer Foundation link: $($f.Name)"
  } else {
    Write-Host "OK: $($f.Name)"
  }
}
Write-Host "Done."
