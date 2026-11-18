"""
create_submission_zip.py - Assembles Assignment_3_Project_Repository.zip
Strictly includes required project source files and excludes virtual environments, git, and caches.
"""

import os
import zipfile

zip_filename = "Assignment_3_Project_Repository.zip"
submission_dir = "Assignment_3_Submission"

os.makedirs(submission_dir, exist_ok=True)

# Define exact file inclusions and patterns
include_files = [
    "Main.py",
    "resume_utils.py",
    "README.md",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    ".github/workflows/ci-cd.yml",
    "tests/__init__.py",
    "tests/test_screening.py",
    "architecture_diagram.svg",
    "cicd_diagram.svg",
    "cloud_architecture_diagram.svg"
]

# Include sample resumes directory
resume_samples = []
for root, dirs, files in os.walk("resumeSamples"):
    for file in files:
        if file.endswith(".pdf"):
            resume_samples.append(os.path.join(root, file))

all_files = include_files + resume_samples

# Create zip in root and in submission directory
for target_zip in [zip_filename, os.path.join(submission_dir, zip_filename)]:
    with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in all_files:
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=file_path)
                print(f"Added to {target_zip}: {file_path}")
            else:
                print(f"WARNING: File {file_path} not found!")

# Copy PDF to submission directory as well
import shutil
shutil.copy2("Assignment_3_DevOps_and_Cloud.pdf", os.path.join(submission_dir, "Assignment_3_DevOps_and_Cloud.pdf"))

print("\n--- Package Verification ---")
with zipfile.ZipFile(zip_filename, 'r') as zipf:
    print(f"Total entries in {zip_filename}: {len(zipf.namelist())}")
    for item in sorted(zipf.namelist()):
        print(f" - {item}")

print(f"\nCreated successfully in {submission_dir}/")
