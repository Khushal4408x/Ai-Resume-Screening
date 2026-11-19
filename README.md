# AI-Powered Resume Screening and Ranking System

A cloud-ready, containerized Python web application that analyzes PDF candidate resumes against technical job descriptions and objectively ranks candidates using classical **TF-IDF Vectorization** and **Cosine Similarity**. Built with **Python 3.12**, **Streamlit**, **PyPDF2**, and **Scikit-learn**, this project provides a deterministic, lightweight, and privacy-preserving candidate screening tool.

---

## 📑 Project Documentation & Assignment Artifacts

- **Academic Assignment Report (PDF):** [`Assignment_3_Submission/Assignment_3_DevOps_Cloud_Computing.pdf`](Assignment_3_Submission/Assignment_3_DevOps_Cloud_Computing.pdf) (Comprehensive 8-page report answering Q1–Q5 with complete diagrams, Well-Architected evaluation, privacy analysis, and testing verification).
- **ERP Form Answers:** [`Assignment_3_Submission/Form_Answers.md`](Assignment_3_Submission/Form_Answers.md)
- **Submission Overview:** [`Assignment_3_Submission/README_Submission.md`](Assignment_3_Submission/README_Submission.md)
- **Verified Docker Screenshot:** [`Assignment_3_Submission/screenshots/02_application_running_in_docker.png`](Assignment_3_Submission/screenshots/02_application_running_in_docker.png)

---

## 🚀 Features

- **Pure In-Memory PDF Extraction:** Extracts raw text from multi-page PDF resumes purely in RAM via `PyPDF2` using `io.BytesIO` streams (zero disk persistence, GDPR Article 17 / DPDP Act 2023 compliant).
- **Mathematical Information Retrieval:** Transforms job descriptions and candidate resumes into TF-IDF vector space with L2 normalization (deterministic, reproducible, zero LLM hallucinations).
- **Geometric Similarity Scoring:** Computes pairwise cosine similarity angles to generate scores from 0.00% to 100.00%.
- **Dynamic Leaderboard:** Ranks candidates in descending order with visual color-coded badges (*High Match* $\ge 75\%$, *Good Match* $50\text{--}74\%$, *Moderate Match* $30\text{--}49\%$, *Low Match* $< 30\%$).
- **Clean UTF-8 CSV Export:** Downloads candidate rankings with timestamps without polluting data with HTML markup.
- **Enterprise Containerization:** OCI-compliant Docker container based on `python:3.12-slim` running under an unprivileged user (`appuser`, UID 1000) with integrated container healthchecks.
- **Automated CI/CD Pipeline:** Fully configured GitHub Actions workflow for linting, syntax compilation, 13 automated unit tests, Docker build verification, and Amazon ECR publishing.

---

## 🛠️ Technology Stack

| Component | Technology | Version / Specification | Role in Project |
|---|---|---|---|
| **Runtime** | Python | 3.12+ | Core programming runtime and math execution |
| **Frontend UI** | Streamlit | 1.43+ | Reactive single-page web dashboard and file upload |
| **PDF Extraction** | PyPDF2 | 3.0+ | In-memory stream parsing of multi-page PDF files |
| **ML / Math** | Scikit-learn | 1.6+ | TF-IDF Vectorization and Cosine Similarity |
| **Data Processing** | Pandas & NumPy | Modern release | Tabular ranking, sorting, and CSV serialization |
| **Testing** | Pytest | 9.2+ | Automated unit test suite (13 test cases) |
| **Containerization**| Docker | OCI Compliant | `python:3.12-slim` image, non-root user `appuser` |
| **CI/CD** | GitHub Actions | Ubuntu Latest | Continuous linting, testing, container builds, and ECR publish |
| **Cloud Registry** | Amazon ECR | `ap-south-1` | Published image: `700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening` |
| **Cloud Target** | AWS EC2 / ALB | Proposed / Ready | Multi-AZ Auto-Scaling Group behind Application Load Balancer |

---

## 📂 Project Structure

```text
Ai-Resume-Screening/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions CI/CD Pipeline (Test, Build, Deploy)
├── tests/
│   ├── __init__.py
│   └── test_screening.py         # 13 Automated Pytest Unit Tests
├── Assignment_3_Submission/
│   ├── Assignment_3_DevOps_Cloud_Computing.pdf # 8-Page Academic PDF Report
│   ├── Project_Repository.zip    # Clean zip archive of project repository
│   ├── Form_Answers.md           # Answers for ERP portal submission fields
│   ├── README_Submission.md      # Submission overview & student verification checklist
│   └── screenshots/
│       └── 02_application_running_in_docker.png # Verified Docker container screenshot
├── resumeSamples/                # Sample resumes for testing and demonstrations
├── Main.py                       # Streamlit UI & interaction entry point
├── resume_utils.py               # Pure business logic & algorithm module
├── Dockerfile                    # Multi-stage/lean production Dockerfile (non-root)
├── .dockerignore                 # Excludes .git, .venv, caches, secrets from image
├── requirements.txt              # Pinned application dependencies
├── architecture_diagram.svg      # Subsystem architecture & data flow diagram
├── cicd_diagram.svg              # CI/CD pipeline & automated test lifecycle diagram
├── cloud_architecture_diagram.svg# Multi-AZ AWS production cloud blueprint
└── README.md                     # Comprehensive project documentation
```

---

## ⚙️ Local Setup and Installation

### Prerequisites

- Python 3.12 or later
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Khushal4408x/Ai-Resume-Screening.git
cd Ai-Resume-Screening
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest flake8
```

### 4. Run the Streamlit Application Locally

```bash
streamlit run Main.py
```

The application will be accessible at: `http://localhost:8501`

---

## 🧪 Automated Testing

The project includes an automated test suite with **13 test cases** implemented with `pytest` in `tests/test_screening.py`:

```bash
# Run tests with verbose output
pytest tests/ -v
```

### Test Coverage Highlights:
1. **PDF Text Extraction:** Tests valid multi-page PDFs, empty byte streams, and corrupted file handling.
2. **Mathematical Correctness:** Tests score bounds ($0.0 \le \text{Score} \le 100.0$), identical document match ($\approx 100\%$), disjoint vocabulary ($0.0\%$), and empty JD/resumes edge cases.
3. **Semantic Ranking Order:** Tests that strong-match resumes rank strictly higher than moderate or unrelated resumes.
4. **Export Logic:** Tests score-to-badge mappings, DataFrame sorting, and CSV serialization without HTML tags.

---

## 🐳 Docker Containerization

The application is containerized using an enterprise-ready `Dockerfile`:
- Base: `python:3.12-slim`
- User: Non-root `appuser` (UID 1000) for security hardening
- Binding: `0.0.0.0:8501`
- Built-in Health Check: Polling `http://localhost:8501/_stcore/health`

### Build the Docker Image:

```bash
docker build -t ai-resume-screening:latest .
```

### Run the Docker Container:

```bash
docker run -d --name ai-resume-app -p 8501:8501 ai-resume-screening:latest
```

Verify the container status:

```bash
docker ps
curl http://localhost:8501/_stcore/health
```

Access the application in your browser at `http://localhost:8501`.

---

## 🔄 CI/CD Automation (GitHub Actions)

The workflow defined in `.github/workflows/ci-cd.yml` automates the release pipeline:

1. **Lint & Test Stage:**
   - Checks out code on `ubuntu-latest`.
   - Compiles Python bytecode and validates syntax with `flake8`.
   - Executes all 13 unit tests via `pytest`.
2. **Container Build & Validation Stage:**
   - Builds the Docker image via Docker Buildx.
   - Spins up a test container and probes the `/_stcore/health` endpoint.
3. **Publish & Deploy Stage (Amazon ECR):**
   - Authenticates to AWS using OpenID Connect (OIDC) role assumptions (zero static credentials).
   - Tags and pushes images to Amazon ECR.

---

## ☁️ AWS Cloud Architecture & ECR Publishing

### Active Amazon ECR Repository:
- **Registry:** `700017004419.dkr.ecr.ap-south-1.amazonaws.com`
- **Repository:** `ai-resume-screening`
- **Region:** `ap-south-1` (Mumbai)
- **Published Tags:** `:latest`, `:v1.0.0`
- **Verified Digest:** `sha256:ea5512e14d23cc6b37b2bd3edc9f9aa27ad48f7a233420f90927803abcee9197`

### Production Architecture Blueprint:
- **VPC & Subnets:** Isolated Amazon VPC (`10.0.0.0/16`) across 2 Availability Zones (`ap-south-1a`, `ap-south-1b`).
- **Load Balancing:** Internet-facing AWS Application Load Balancer (ALB) terminating HTTPS/TLS 1.3.
- **Compute:** Auto-Scaling Group of EC2 instances in private subnets pulling immutable images from Amazon ECR.
- **Security:** Strict IAM least-privilege roles, OIDC federated identity, Security Groups restricting ingress exclusively to ALB port 8501.
- **Monitoring:** AWS CloudWatch Metrics, CloudWatch Logs (`awslogs` driver), and CloudWatch Synthetics synthetic health canaries.

---

## 🔒 Security & Candidate Privacy

- **Zero Disk Persistence:** Uploaded PDF resumes are read directly into Python memory (`io.BytesIO`) and discarded upon garbage collection.
- **No Database Footprint:** No candidate names, email addresses, phone numbers, or work history are saved to disk or external databases.
- **Regulatory Alignment:** Adheres to **GDPR Article 17** ("Right to Erasure") and India's **Digital Personal Data Protection (DPDP) Act 2023**.

---

## ⚠️ Known Limitations & Future Roadmap

1. **Keyword-Centric Matching:** TF-IDF captures lexical overlap rather than deep semantic contextual nuances (e.g., synonyms without common terms).
2. **Scanned PDF Handling:** Resumes consisting solely of scanned bitmap images require an upstream OCR engine (e.g., AWS Textract or Tesseract).
3. **Future Scaling (Kubernetes / EKS):** For massive enterprise concurrency, decompose the frontend from background batch processing using Amazon EKS and Celery/Redis queues.

---

## 👨‍🎓 Academic Submission Metadata

- **Course:** DevOps and Cloud Computing (BCDS0501)
- **Unit & Assignment:** Unit 4 — Assignment 3 (Session 2026–27)
- **Institution:** Noida Institute of Engineering and Technology (NIET), Greater Noida
- **Student Name:** Khushal Singh
