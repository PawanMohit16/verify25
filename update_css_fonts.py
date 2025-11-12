#!/usr/bin/env python3
"""
Update all style.css files for hfest events to use Atkinson Hyperlegible Bold font
"""

import re
from pathlib import Path

EVENTS = ['hfestM', 'hfestOC', 'hfestP', 'hfestSM', 'hfestW']
docs_dir = Path(__file__).parent / 'docs'

print("=" * 60)
print("🎨 Updating CSS files with Atkinson Hyperlegible Bold font")
print("=" * 60)

for event in EVENTS:
    style_path = docs_dir / event / 'style.css'
    
    if not style_path.exists():
        print(f"⚠️  Not found: {style_path}")
        continue
    
    print(f"\nUpdating {event}/style.css...")
    
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add Google Fonts import if not already there
    if '@import url' not in content or 'Atkinson+Hyperlegible' not in content:
        # Find the body or first @font-face and add the import
        if '@font-face' in content:
            content = content.replace(
                '@font-face',
                "@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@700&display=swap');\n\n@font-face"
            )
        else:
            content = "body {\n    max-width: 100%;\n}\n\n@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@700&display=swap');\n\n" + content
    
    # Update #name-element styling
    old_name_pattern = r'#name-element\s*\{\s*font-size:\s*62\.0px;\s*\}'
    new_name_style = '''#name-element {
    font-size: 62.0px;
    font-family: 'Atkinson Hyperlegible', sans-serif;
    font-weight: 700;
}'''
    
    if re.search(old_name_pattern, content):
        content = re.sub(old_name_pattern, new_name_style, content)
        print(f"  ✅ Updated #name-element styling")
    else:
        # If pattern not found, try to add it after .baskvile
        if '.baskvile' in content:
            content = content.replace(
                '.baskvile {',
                new_name_style + '\n\n.baskvile {'
            )
            print(f"  ✅ Added #name-element styling")
    
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Successfully updated")

print("\n" + "=" * 60)
print("✅ All CSS files updated with Atkinson Hyperlegible Bold!")
print("=" * 60)
