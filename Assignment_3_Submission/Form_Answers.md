# College Assignment ERP Submission — Form Answers
**Subject:** DevOps and Cloud Computing (BCDS0501) — Unit 4, Assignment 3  
**Session:** 2026–27  
**Institution:** Noida Institute of Engineering and Technology (NIET), Greater Noida  
**Student Name:** Khushal Singh  
**University Roll No:** `2101330100XXX` *(Please enter your official university roll number in the ERP portal)*

---

## Instructions for the Student
Copy and paste the exact text blocks below into the corresponding fields on your College ERP / Google Classroom / LMS assignment submission portal.

---

### 1. Project Title
```text
AI-Powered Resume Screening and Ranking System: Cloud-Native Containerization, Automated CI/CD, and AWS Architecture
```

---

### 2. Problem Statement
```text
In contemporary technical recruitment, talent acquisition teams receive hundreds of unstructured PDF resumes for every job opening. Manual resume evaluation is labor-intensive, error-prone, slow, and vulnerable to unconscious human bias. Existing enterprise solutions are often opaque, expensive, or compromise candidate privacy by storing sensitive Personally Identifiable Information (PII) on permanent third-party storage.

This project addresses these challenges by developing a lightweight, deterministic, privacy-preserving resume screening application that extracts text from multi-page PDF resumes purely in RAM, computes objective mathematical similarity scores against a job description using TF-IDF vectorization and cosine similarity, and presents an interactive ranked candidate leaderboard with UTF-8 CSV export. Furthermore, the system implements a modern DevOps lifecycle: containerization with Docker, automated linting and 13 unit tests via GitHub Actions CI/CD, container registry publishing on Amazon ECR, and an AWS cloud architecture evaluation.
```

---

### 3. GitHub Repository URL
```text
https://github.com/Khushal4408x/Ai-Resume-Screening.git
```

---

### 4. Technology Stack
```text
- Programming Language & Runtime: Python 3.12+
- Web Framework / Frontend: Streamlit 1.43+
- PDF Extraction Engine: PyPDF2 3.0+ (pure in-memory io.BytesIO parsing)
- Mathematical IR & Scoring: Scikit-learn (TfidfVectorizer, cosine_similarity)
- Data Processing & Export: Pandas & NumPy
- Automated Testing Framework: Pytest 9.2+ (13 automated unit tests)
- Containerization: Docker (python:3.12-slim base, unprivileged appuser UID 1000, internal healthcheck)
- CI/CD Automation: GitHub Actions (.github/workflows/ci-cd.yml)
- Cloud Container Registry: Amazon Elastic Container Registry (ECR) [ap-south-1]
- Proposed Cloud Production Target: AWS EC2 Auto-Scaling Group behind Application Load Balancer
```

---

### 5. Selected Cloud Platform & Region
```text
- Cloud Platform: Amazon Web Services (AWS)
- AWS Region: ap-south-1 (Asia Pacific - Mumbai)
- Target Account ID: 700017004419
- Amazon ECR URI: 700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening
- Pushed Image Tags: :latest, :v1.0.0
- Verified Digest: sha256:ea5512e14d23cc6b37b2bd3edc9f9aa27ad48f7a233420f90927803abcee9197
```

---

### 6. DevOps Tool Integration Summary
```text
1. Git: Distributed local version control tracking all commits, branches, and ignoring cache/credentials via .gitignore.
2. GitHub: Central remote origin repository (Khushal4408x/Ai-Resume-Screening) hosting source code and dispatching CI/CD webhooks.
3. Docker: Container engine packaging Python 3.12 runtime, dependencies, and code into an immutable 254MB container running as non-root user 'appuser' on port 8501.
4. GitHub Actions: Automated CI/CD orchestrator executing linting, bytecode compilation, 13 pytest tests, Docker build validation, and keyless AWS OIDC authentication for Amazon ECR publishing.
5. Amazon ECR: Fully managed, private container registry hosting published application images.
6. AWS EC2 (Proposed): Target virtual machine hosting containers inside private VPC subnets behind an Application Load Balancer.
```

---

### 7. CI/CD Workflow Stages
```text
The CI/CD pipeline is implemented in '.github/workflows/ci-cd.yml' and comprises three sequential stages:
1. Stage 1 (test): Checks out code, sets up Python 3.12, installs dependencies, validates syntax via py_compile & flake8, and executes 13 pytest unit tests covering PDF parsing, TF-IDF scoring, and ranking order.
2. Stage 2 (build-container): Sets up Docker Buildx, builds the OCI image, launches a background container, verifies the Streamlit '/_stcore/health' endpoint, and confirms HTTP 200 OK.
3. Stage 3 (deploy): Triggered on main branch; authenticates to AWS using OpenID Connect (OIDC) federated role assumption without static credentials, logs into Amazon ECR, tags images with commit SHA and :latest, and pushes the image to ap-south-1.
```

---

### 8. Deployed Application URL / AWS Deployment Status
```text
Deployment Status: Container image is successfully built, verified, and published to Amazon ECR (700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening:latest). 

The AWS EC2 production deployment scripts, CloudWatch configurations, and security group architectures are fully prepared. In strict adherence to institutional safety guidelines and to prevent unapproved cloud billing charges, live EC2 virtual instances have not been provisioned on the student's personal AWS account without explicit cost sign-off. The application was verified locally running inside Docker on port 8501 (verified screenshot included in submission package).
```

---

### 9. Key Implementation Challenges & Technical Resolutions
```text
1. Challenge: High-concurrency data privacy and candidate PII compliance.
   Resolution: Refactored PDF parsing to operate purely in-memory using io.BytesIO byte streams. No resume files, candidate names, or contact details are written to server disk or persistent databases, ensuring native compliance with GDPR Article 17 and India's DPDP Act 2023.

2. Challenge: Python 3.11 vs. Python 3.12 dependency compatibility.
   Resolution: Pinned NumPy 2.5.4 requires Python >= 3.12. Upgraded Docker base image from python:3.11-slim to python:3.12-slim, ensuring clean dependency resolution and reproducible multi-platform builds.

3. Challenge: Container security and root privilege vulnerabilities.
   Resolution: Enhanced Dockerfile with an unprivileged system user ('appuser', UID 1000) and group, avoiding default root execution and adhering to container security best practices.

4. Challenge: Secretless CI/CD authentication to AWS.
   Resolution: Designed GitHub Actions deploy stage to use AWS OpenID Connect (OIDC) federated identity, completely eliminating the need to store long-lived AWS IAM access keys in GitHub Secrets.

5. Challenge: Modular code structure for automated unit testing.
   Resolution: Decoupled UI logic from business math by creating 'resume_utils.py'. This allowed authoring 13 comprehensive pytest test cases in 'tests/test_screening.py' that run in 1.73 seconds without needing a live Streamlit browser session.
```

---

### 10. List of Submission Attachments
```text
1. Academic PDF Report: Assignment_3_Submission/Assignment_3_DevOps_Cloud_Computing.pdf (8 pages, complete Q1-Q5 answers, 3 SVG diagrams, Figure 5.2 screenshot)
2. Project Repository ZIP: Assignment_3_Submission/Project_Repository.zip (Complete source code, Dockerfile, GitHub Actions workflow, 13 pytest tests, sample resumes; excluding .git, .venv, caches, credentials)
3. Verified Docker Screenshot: Assignment_3_Submission/screenshots/02_application_running_in_docker.png (187KB genuine evidence screenshot of running application)
```

---

### 11. Student Declaration Note
*(Review and check this box manually in the ERP portal)*:
```text
I hereby declare that the work submitted for Assignment 3 of DevOps and Cloud Computing (BCDS0501) is my original work based on my project repository. All technical implementations, Docker containerization, automated testing suites, and AWS cloud evaluations have been executed and documented honestly in accordance with the university code of conduct.
```
