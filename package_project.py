"""
Packages the complete lab3b project into a clean .zip file for submission.
Excludes bytecode cache (__pycache__, *.pyc).
"""

import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ZIP_NAME = BASE_DIR / 'Lab3B_Project.zip'

EXCLUDE_DIRS = {'__pycache__', '.git', 'html'}
EXCLUDE_EXTS = {'.pyc', '.pyo'}


def create_zip():
    print(f"Creating submission zip: {ZIP_NAME.name}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in EXCLUDE_EXTS or file_path.name == 'Lab3B_Project.zip':
                    continue

                rel_path = file_path.relative_to(BASE_DIR)
                zipf.write(file_path, arcname=str(rel_path))
                print(f"  Added: {rel_path}")

    print(f"\nZip archive successfully created: {ZIP_NAME} ({ZIP_NAME.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == '__main__':
    create_zip()
