#!/usr/bin/env python3
"""Hotfix for missing import"""
import os

with open('app.py', 'r') as f:
    lines = f.readlines()

# Find where to insert shutil (after os import)
fixed_lines = []
shutil_added = False

for line in lines:
    fixed_lines.append(line)
    if 'import os' in line and not shutil_added:
        fixed_lines.append('import shutil
')
        shutil_added = True

with open('app.py', 'w') as f:
    f.writelines(fixed_lines)

print("✓ Fixed! Added missing 'import shutil'")
print("You can now run: python app.py")
