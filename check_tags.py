import re
import os

def find_multiline_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    multiline_vars = re.findall(r'\{\{[^}]*\n[^}]*\}\}', content)
    multiline_tags = re.findall(r'\{\%[^%]*\n[^%]*\%\}', content)
    
    return multiline_vars + multiline_tags

template_dir = r'templates'

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            problems = find_multiline_tags(path)
            if problems:
                print(f"File: {path}")
                for p in problems:
                    # Show only the first 50 chars of the problem tag to avoid large output
                    tag_display = p.replace('\n', '\\n')[:100]
                    print(f"  Tag: {tag_display}...")

print("Scan complete.")
