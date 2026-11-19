# DevOps and Cloud Computing — Assignment 3 Submission Package
**Course:** DevOps and Cloud Computing (BCDS0501) — Unit 4  
**Session:** 2026–27  
**Institution:** Noida Institute of Engineering and Technology (NIET), Greater Noida  
**Student Name:** Khushal Singh  
**Project:** AI-Powered Resume Screening and Ranking System  
**Repository:** https://github.com/Khushal4408x/Ai-Resume-Screening.git  

---

## 📦 Directory Contents

```text
Assignment_3_Submission/
├── Assignment_3_DevOps_Cloud_Computing.pdf # Primary deliverable: Comprehensive 8-page academic PDF report
├── Project_Repository.zip                  # Clean archive of project repository for ERP upload
├── Form_Answers.md                         # Copy-paste answers for college ERP portal fields
├── README_Submission.md                    # This document (submission checklist & ERP guide)
└── screenshots/
    └── 02_application_running_in_docker.png # Genuine verified screenshot of Streamlit app running in Docker
```

---

## 📋 Deliverables Verification Status

| Deliverable | File Path | Status | Verification Detail |
|---|---|---|---|
| **Question 1–5 Academic PDF** | `Assignment_3_Submission/Assignment_3_DevOps_Cloud_Computing.pdf` | ✅ **Complete** | Exactly 8 pages, unencrypted, containing all 5 questions, 3 vector SVG diagrams, Figure 5.2 screenshot, Well-Architected Framework evaluation, candidate data privacy analysis, and academic references. |
| **Project Repository Archive** | `Assignment_3_Submission/Project_Repository.zip` | ✅ **Complete** | Clean ZIP archive containing all source files (`Main.py`, `resume_utils.py`), `Dockerfile`, `.dockerignore`, `.github/workflows/ci-cd.yml`, `tests/`, `resumeSamples/`, `requirements.txt`, and diagrams. Excludes `.git`, `.venv`, caches, and secrets. |
| **Genuine Evidence Screenshot** | `Assignment_3_Submission/screenshots/02_application_running_in_docker.png` | ✅ **Complete** | 187KB genuine screenshot capturing the running Streamlit web application inside Docker on port 8501. |
| **ERP Portal Form Answers** | `Assignment_3_Submission/Form_Answers.md` | ✅ **Complete** | Formatted answers for ERP text fields (Problem Statement, Tech Stack, Cloud Evaluation, CI/CD stages, Challenges & Resolutions). |
| **Automated Test Suite** | `tests/test_screening.py` | ✅ **Passed** | 13/13 tests passed via Pytest in 1.73s covering PDF extraction, TF-IDF scoring bounds, ranking order, and CSV export. |
| **Docker Containerization** | `Dockerfile`, `.dockerignore` | ✅ **Verified** | `python:3.12-slim` image, non-root user `appuser` (UID 1000), port 8501, 0.0.0.0 binding, internal healthcheck on `/_stcore/health`. |
| **Amazon ECR Publishing** | AWS Region `ap-south-1` | ✅ **Published** | Pushed to `700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening:latest` and `:v1.0.0` (Digest: `sha256:ea5512e14d23cc6b37b2bd3edc9f9aa27ad48f7a233420f90927803abcee9197`). |
| **AWS EC2 Production Deployment** | AWS Architecture Blueprint | ⏳ **Prepared** | Production architecture and user-data scripts designed; live instance launch held pending explicit student sign-off to prevent unapproved cloud costs. |

---

## 🚀 Step-by-Step Student ERP Submission Instructions

Follow these steps to submit your assignment on the college ERP portal (or Google Classroom / LMS):

1. **Log in to the College ERP Portal:**
   - Open your browser and log into your student portal.
   - Navigate to **DevOps and Cloud Computing (BCDS0501)** &rarr; **Assignments** &rarr; **Unit 4 Assignment 3**.

2. **Upload the Academic Report PDF:**
   - Click **Attach File** or **Upload Document**.
   - Select and upload:
     ```text
     Assignment_3_Submission/Assignment_3_DevOps_Cloud_Computing.pdf
     ```
   - Verify that the uploaded file displays 8 pages.

3. **Upload the Project Repository ZIP:**
   - Click **Attach Additional File** or **Upload Project Code (ZIP)**.
   - Select and upload:
     ```text
     Assignment_3_Submission/Project_Repository.zip
     ```

4. **Fill in the Online Submission Form:**
   - Open [`Assignment_3_Submission/Form_Answers.md`](Form_Answers.md).
   - Copy and paste the corresponding sections into each form field:
     - **Project Title:** See Section 1.
     - **Problem Statement:** See Section 2.
     - **GitHub Repository URL:** `https://github.com/Khushal4408x/Ai-Resume-Screening.git`
     - **Tech Stack:** See Section 4.
     - **Cloud Platform & ECR URI:** See Section 5.
     - **DevOps Tools & CI/CD Workflow:** See Section 6 & 7.
     - **Challenges and Resolutions:** See Section 9.

5. **Upload the Evidence Screenshot (if prompted for screenshot/image attachment):**
   - If the portal provides a separate screenshot upload field, upload:
     ```text
     Assignment_3_Submission/screenshots/02_application_running_in_docker.png
     ```

6. **Review and Submit:**
   - Verify your Roll Number and Name.
   - Read and check the **Student Declaration** checkbox.
   - Click **Submit Assignment** and save your submission confirmation receipt.
