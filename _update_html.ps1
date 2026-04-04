$dir = 'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation\'
$files = Get-ChildItem "$dir*.html"

foreach ($f in $files) {
  $content = [System.IO.File]::ReadAllText($f.FullName)

  # Skip if legal block already added
  if ($content -match '/privacy-policy">Privacy Policy') {
    Write-Host "SKIP (already has legal links): $($f.Name)"
    continue
  }

  # ── Footer: insert Legal sub-section right after the Foundation </ul>
  # The unique anchor is the executive-bureau line followed by </ul> then </div> then footer-nav
  $footerSearch = '            <li><a href="executive-bureau.html">Executive Bureau</a></li>
          </ul>
        </div>
        <div class="footer-nav">'

  $footerReplace = '            <li><a href="executive-bureau.html">Executive Bureau</a></li>
          </ul>
          <p class="footer-col-title" style="margin-top:1.5rem;">Legal</p>
          <ul>
            <li><a href="/privacy-policy">Privacy Policy</a></li>
            <li><a href="/terms">Terms of Service</a></li>
            <li><a href="/data-deletion">Data Deletion</a></li>
          </ul>
        </div>
        <div class="footer-nav">'

  $content = $content.Replace($footerSearch, $footerReplace)

  # ── Nav: change Legal href from legal-recognition.html to /privacy-policy
  # Handles both plain and class="active" variants
  $content = $content -replace 'href="legal-recognition\.html"( class="active")?>Legal', 'href="/privacy-policy">Legal'

  [System.IO.File]::WriteAllText($f.FullName, $content, [System.Text.Encoding]::UTF8)
  Write-Host "UPDATED: $($f.Name)"
}
Write-Host "Done."
