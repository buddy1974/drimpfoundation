import os
import re

directory = r'C:\Users\loneb\Documents\ai-software-dev\projects\drimpfoundation'
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in sorted(html_files):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the footer-links block and within it, fix any
    # href="/privacy-policy">Legal</a> back to href="legal-recognition.html">Legal</a>
    # This only touches the Foundation column, not the nav or the new Legal section we added.
    #
    # Strategy: find the footer-links div, then within it find the Foundation <ul>
    # (before the Legal footer-col-title we added), and fix the href there.

    # The footer-links block looks like:
    #   <div class="footer-links">
    #     <p class="footer-col-title">Foundation</p>
    #     <ul>
    #       ... about.html link ...
    #       ... legal link (possibly wrong) ...
    #       ... executive-bureau link ...
    #     </ul>
    #     <p class="footer-col-title" ...>Legal</p>   <-- we added this
    #     <ul> ... our 3 new links ... </ul>
    #   </div>

    def fix_footer_links(m):
        block = m.group(0)
        # Split at the Legal footer-col-title we added (which is our marker)
        parts = re.split(r'<p class="footer-col-title"[^>]*>Legal</p>', block, maxsplit=1)
        if len(parts) < 2:
            return block  # no Legal section found, skip
        foundation_part = parts[0]
        legal_part = parts[1]
        # In the foundation part, fix href="/privacy-policy">Legal</a> → legal-recognition.html
        foundation_fixed = foundation_part.replace(
            'href="/privacy-policy">Legal</a>',
            'href="legal-recognition.html">Legal</a>'
        )
        # Also fix href="/privacy-policy">Legal Recognition</a> just in case
        foundation_fixed = foundation_fixed.replace(
            'href="/privacy-policy">Legal Recognition</a>',
            'href="legal-recognition.html">Legal Recognition</a>'
        )
        # Reconstruct
        return foundation_fixed + '<p class="footer-col-title"' + re.search(
            r'<p class="footer-col-title"[^>]*>Legal</p>', block
        ).group(0)[len('<p class="footer-col-title"'):] + legal_part

    # Match the entire footer-links div
    pattern = r'<div class="footer-links">[\s\S]*?</div>\s*\n\s*<div class="footer-nav">'
    new_content = re.sub(pattern, fix_footer_links, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'FIXED: {filename}')
    else:
        print(f'OK:    {filename}')

print('Done.')
