import re
import os

directory = r'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation'

# Pages with Foundation-style footer (already fixed)
foundation_pages = {
    'legal-recognition.html',
    'executive-bureau.html',
    'privacy-policy.html',
    'terms.html',
    'data-deletion.html',
}

legal_section = (
    '\n          <p class="footer-col-title" style="margin-top:1.5rem;">Legal</p>\n'
    '          <ul>\n'
    '            <li><a href="/privacy-policy">Privacy Policy</a></li>\n'
    '            <li><a href="/terms">Terms of Service</a></li>\n'
    '            <li><a href="/data-deletion">Data Deletion</a></li>\n'
    '          </ul>'
)

html_files = sorted([f for f in os.listdir(directory) if f.endswith('.html')])

for filename in html_files:
    if filename in foundation_pages:
        print(f'SKIP (Foundation-style): {filename}')
        continue

    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into header section and footer section at <footer class="footer">
    footer_split = content.split('<footer class="footer">', 1)
    if len(footer_split) != 2:
        print(f'WARN: no footer found in {filename}')
        continue

    pre_footer = footer_split[0]
    footer_content = '<footer class="footer">' + footer_split[1]

    # 1. In the footer only: restore Legal link from /privacy-policy back to legal-recognition.html
    footer_fixed = footer_content.replace(
        'href="/privacy-policy">Legal</a>',
        'href="legal-recognition.html">Legal</a>'
    )

    # 2. Add Legal section after the Navigate </ul> in footer-nav, if not already added
    if '/privacy-policy">Privacy Policy' not in footer_fixed:
        # Find the Navigate </ul> closing tag in footer-nav and insert after it
        # The pattern is </ul> followed by </div> (closing footer-nav) within the footer
        # We look for the last </ul> before </div> in the footer-nav block
        footer_fixed = re.sub(
            r'(<p class="footer-col-title">Navigate</p>\s*<ul>[\s\S]*?</ul>)',
            r'\1' + legal_section,
            footer_fixed,
            count=1
        )

    new_content = pre_footer + footer_fixed

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'FIXED: {filename}')
    else:
        print(f'NO CHANGE: {filename}')

print('\nDone.')
