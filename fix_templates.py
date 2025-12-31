import re
import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix case 1: {{ var|default:"val" }} spanning multiple lines
    # Patterns like {{ ... \n ... }}
    # We want to catch everything between {{ and }} and remove newlines/extra spaces
    def normalize_tag(match):
        tag_content = match.group(1)
        # Remove newlines and collapse multiple spaces inside the tag
        normalized = re.sub(r'\s+', ' ', tag_content).strip()
        # Also specifically fix the default: spaces if they exist
        normalized = re.sub(r'\|\s*default\s*:\s*', '|default:', normalized)
        return '{{ ' + normalized + ' }}'

    new_content = re.sub(r'\{\{(.*?)\}\}', normalize_tag, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {filepath}")

files_to_fix = [
    r'c:\Users\patri\OneDrive\Desktop\@SOLVIT\Python\Studying Project\Smart_Logistic_Project\templates\logistics\dashboard_v2.html',
    r'c:\Users\patri\OneDrive\Desktop\@SOLVIT\Python\Studying Project\Smart_Logistic_Project\templates\logistics\dispatcher_deliveries.html'
]

for fp in files_to_fix:
    if os.path.exists(fp):
        fix_file(fp)
    else:
        print(f"File not found: {fp}")
