import re
import os

directory = r'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation'

legal_section = (
    '\n          <p class="footer-col-title" style="margin-top:1.5rem;">Legal</p>\n'
    '          <ul>\n'
    '            <li><a href="/privacy-policy">Privacy Policy</a></li>\n'
    '            <li><a href="/terms">Terms of Service</a></li>\n'
    '            <li><a href="/data-deletion">Data Deletion</a></li>\n'
    '          </ul>'
)

target_files = ['7-pillars.html', 'blossom-life-academy.html']

for filename in target_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/privacy-policy">Privacy Policy' in content:
        print(f'SKIP (already done): {filename}')
        continue

    # Split at footer
    parts = content.split('<footer class="footer">', 1)
    if len(parts) != 2:
        print(f'WARN: no footer in {filename}')
        continue

    footer_content = '<footer class="footer">' + parts[1]

    # These pages have footer-nav with "Foundation" title
    # Add Legal section after the Foundation </ul>
    footer_fixed = re.sub(
        r'(<p class="footer-col-title">Foundation</p>\s*<ul>[\s\S]*?</ul>)',
        r'\1' + legal_section,
        footer_content,
        count=1
    )

    new_content = parts[0] + footer_fixed

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'FIXED: {filename}')
    else:
        print(f'NO CHANGE: {filename} - pattern not found')

print('Done.')
