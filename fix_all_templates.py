import re
import os

def fix_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize {{ ... }}
    def normalize_var(match):
        tag_content = match.group(1)
        normalized = re.sub(r'\s+', ' ', tag_content).strip()
        normalized = re.sub(r'\|\s*default\s*:\s*', '|default:', normalized)
        return '{{ ' + normalized + ' }}'

    # Normalize {% ... %}
    def normalize_tag(match):
        tag_content = match.group(1)
        normalized = re.sub(r'\s+', ' ', tag_content).strip()
        return '{% ' + normalized + ' %}'

    # First pass: Vars
    new_content = re.sub(r'\{\{(.*?)\}\}', normalize_var, content, flags=re.DOTALL)
    # Second pass: Tags
    new_content = re.sub(r'\{\%(.*?)\%\}', normalize_tag, new_content, flags=re.DOTALL)

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Fixed {filepath}")
    else:
        print(f"  No changes needed for {filepath}")

def find_html_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                yield os.path.join(root, file)

template_dir = r'c:\Users\patri\OneDrive\Desktop\@SOLVIT\Python\Studying Project\Smart_Logistic_Project\templates'

for html_file in find_html_files(template_dir):
    fix_file(html_file)

print("Done.")
