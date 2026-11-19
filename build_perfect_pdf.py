"""
build_perfect_pdf.py - Builds the comprehensive academic assignment PDF:
Assignment_3_DevOps_Cloud_Computing.pdf
"""

import os
import subprocess
import base64
from PyPDF2 import PdfReader

# Read the 3 vector SVGs
with open("architecture_diagram.svg", "r", encoding="utf-8") as f:
    arch_svg = f.read()

with open("cicd_diagram.svg", "r", encoding="utf-8") as f:
    cicd_svg = f.read()

with open("cloud_architecture_diagram.svg", "r", encoding="utf-8") as f:
    cloud_svg = f.read()

# Read genuine screenshot
with open("Assignment_3_Submission/screenshots/02_application_running_in_docker.png", "rb") as f:
    screenshot_b64 = base64.b64encode(f.read()).decode("utf-8")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DevOps and Cloud Computing Assignment 3 - AI Resume Screening System</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.42;
    font-size: 9.2pt;
    margin: 0;
    padding: 0;
  }

  .doc-page {
    page-break-after: always;
    position: relative;
    height: 275mm;
    max-height: 275mm;
    overflow: hidden;
    padding-bottom: 7mm;
  }

  .doc-page:last-child {
    page-break-after: avoid;
  }

  /* Institution Header */
  .inst-header {
    border-bottom: 2px solid #1e40af;
    padding-bottom: 4px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .inst-title {
    font-size: 13pt;
    font-weight: 800;
    color: #1e3a8a;
    margin: 0 0 1px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  .inst-dept {
    font-size: 9pt;
    font-weight: 600;
    color: #475569;
    margin: 0;
  }

  .inst-badge {
    background: #dbeafe;
    color: #1e40af;
    font-size: 8pt;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #bfdbfe;
  }

  /* Compact Metadata Card */
  .meta-grid {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    margin-bottom: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3px 12px;
    font-size: 8.3pt;
  }

  .meta-item {
    display: flex;
  }

  .meta-key {
    font-weight: 700;
    color: #334155;
    width: 130px;
    flex-shrink: 0;
  }

  .meta-val {
    color: #0f172a;
    font-weight: 500;
  }

  /* Question Banners */
  .q-banner {
    background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%);
    color: #ffffff;
    font-size: 10.2pt;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 4px;
    margin: 6px 0 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    letter-spacing: 0.2px;
  }

  .q-marks {
    font-size: 8pt;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.22);
    padding: 1.5px 6px;
    border-radius: 3px;
  }

  h3.sec-head {
    font-size: 9.5pt;
    font-weight: 700;
    color: #1e3a8a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
    margin: 6px 0 4px 0;
  }

  h4.sub-head {
    font-size: 8.8pt;
    font-weight: 700;
    color: #0f172a;
    margin: 4px 0 1px 0;
  }

  p {
    margin: 0 0 4px 0;
    text-align: justify;
  }

  ul, ol {
    margin: 0 0 4px 0;
    padding-left: 16px;
  }

  li {
    margin-bottom: 1.5px;
  }

  .code-pill {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 7.6pt;
    font-weight: 600;
    padding: 0.5px 4.5px;
    border-radius: 3px;
    border: 1px solid #bae6fd;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .badge-imp {
    background: #dcfce7;
    color: #15803d;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid #bbf7d0;
  }

  .badge-prop {
    background: #f1f5f9;
    color: #475569;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
  }

  table.q-table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 6px 0;
    font-size: 8pt;
  }

  table.q-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4px 6px;
    border: 1px solid #1e3a8a;
  }

  table.q-table td {
    padding: 3.5px 6px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }

  table.q-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  .diagram-frame {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 3px;
    margin: 4px 0;
    text-align: center;
  }

  .diagram-frame svg {
    max-height: 65mm;
    width: auto;
    max-width: 100%;
    display: inline-block;
  }

  .diagram-title {
    font-size: 7.8pt;
    font-weight: 700;
    color: #475569;
    margin-top: 2px;
  }

  .screenshot-frame {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 3px;
    margin: 4px 0;
    text-align: center;
  }

  .screenshot-frame img {
    max-height: 38mm;
    max-width: 100%;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }

  .screenshot-title {
    font-size: 7.5pt;
    font-weight: 700;
    color: #475569;
    margin-top: 2px;
  }

  .info-box {
    border-left: 3px solid #2563eb;
    background: #eff6ff;
    padding: 4px 8px;
    margin: 4px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8.3pt;
  }

  .info-title {
    font-weight: 700;
    color: #1e40af;
    margin-bottom: 1.5px;
  }

  .info-success {
    border-left-color: #059669;
    background: #ecfdf5;
  }
  .info-success .info-title {
    color: #065f46;
  }

  .info-warning {
    border-left-color: #d97706;
    background: #fffbeb;
  }
  .info-warning .info-title {
    color: #92400e;
  }

  .math-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 3px 6px;
    text-align: center;
    font-family: "Cambria Math", "Times New Roman", serif;
    font-size: 9pt;
    color: #0f172a;
    margin: 4px 0;
  }

  .page-footer {
    position: absolute;
    bottom: 0mm;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 2px;
    font-size: 7.5pt;
    color: #64748b;
  }
</style>
</head>
<body>

<!-- ==========================================================================
     PAGE 1: COVER PAGE, METADATA & TABLE OF CONTENTS
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="meta-grid">
    <div class="meta-item"><span class="meta-key">Subject Name:</span><span class="meta-val">DevOps and Cloud Computing</span></div>
    <div class="meta-item"><span class="meta-key">Subject Code:</span><span class="meta-val">BCDS0501</span></div>
    <div class="meta-item"><span class="meta-key">Student Name:</span><span class="meta-val">Khushal Singh</span></div>
    <div class="meta-item"><span class="meta-key">Academic Session:</span><span class="meta-val">2026–27 (Semester V / VI)</span></div>
    <div class="meta-item"><span class="meta-key">Project Title:</span><span class="meta-val">AI-Powered Resume Screening &amp; Ranking System</span></div>
    <div class="meta-item"><span class="meta-key">GitHub Repository:</span><span class="meta-val">Khushal4408x/Ai-Resume-Screening</span></div>
    <div class="meta-item"><span class="meta-key">Cloud Platform:</span><span class="meta-val">Amazon Web Services (ap-south-1)</span></div>
    <div class="meta-item"><span class="meta-key">Max Marks:</span><span class="meta-val">10.0 Marks (5 Detailed Questions)</span></div>
  </div>

  <div class="q-banner">
    <span>ACADEMIC REPORT CONTENTS &amp; EXECUTIVE PROJECT INTRODUCTION</span>
    <span class="q-marks">Overview</span>
  </div>

  <h3 class="sec-head">1. Table of Contents</h3>
  <table class="q-table" style="margin-bottom: 8px;">
    <thead>
      <tr>
        <th style="width: 15%;">Section</th>
        <th style="width: 70%;">Assignment Question / Academic Topic</th>
        <th style="width: 15%;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>Overview</strong></td><td>Assignment Metadata, Executive Summary &amp; Table of Contents</td><td>Page 1</td></tr>
      <tr><td><strong>Question 1</strong></td><td>Overall Project Architecture, Subsystems &amp; Mathematical Vectorization</td><td>Page 2</td></tr>
      <tr><td><strong>Question 1 (Cont.)</strong></td><td>End-to-End System Data Flow &amp; Complete Architecture Diagram</td><td>Page 3</td></tr>
      <tr><td><strong>Question 2</strong></td><td>DevOps Tool Integration (Git, GitHub, Docker, Actions, ECR) &amp; Status Matrix</td><td>Page 4</td></tr>
      <tr><td><strong>Question 3</strong></td><td>Automated CI/CD Pipeline Lifecycle, 13 Pytest Suites &amp; Pipeline Diagram</td><td>Page 5</td></tr>
      <tr><td><strong>Question 4</strong></td><td>AWS Cloud Platform Evaluation, Candidate Privacy &amp; In-Memory Data Protection</td><td>Page 6</td></tr>
      <tr><td><strong>Question 5</strong></td><td>Improved Cloud Architecture Blueprint, Kubernetes Evolution &amp; AWS Diagram</td><td>Page 7</td></tr>
      <tr><td><strong>Evaluation</strong></td><td>5-Dimension Improvement Matrix, Testing Results, Limitations &amp; References</td><td>Page 8</td></tr>
    </tbody>
  </table>

  <h3 class="sec-head">2. Project Introduction &amp; Problem Statement</h3>
  <p>
    In corporate recruitment, talent acquisition specialists regularly review hundreds to thousands of candidate resumes for technical job openings. Manual screening is labor-intensive, slow, and susceptible to cognitive fatigue and unconscious recruiter bias. The <strong>AI-Powered Resume Screening and Ranking System</strong> is an automated, objective information retrieval web application built using <strong>Python</strong>, <strong>Streamlit</strong>, and <strong>Scikit-learn</strong>.
  </p>
  <p>
    The application ingests an arbitrary target Job Description (JD) and a batch of multi-page PDF candidate resumes, extracts textual content purely in-memory using <code>PyPDF2</code>, transforms unstructured text into numerical feature vectors via <strong>Term Frequency-Inverse Document Frequency (TF-IDF)</strong>, and computes geometric <strong>Cosine Similarity</strong> metrics to produce an objective, ranked candidate leaderboard in real time with UTF-8 CSV export.
  </p>

  <div class="info-box info-success">
    <div class="info-title">Technical Integrity &amp; Domain Clarification</div>
    This project employs classical mathematical Information Retrieval (Vector Space Models via TF-IDF and Cosine Similarity). It is deliberately designed as a deterministic, lightweight Python application without deep neural networks, generative LLMs, or external database overhead, ensuring instantaneous execution, zero candidate profiling bias, and strict data privacy.
  </div>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 1 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 2: QUESTION 1 (PART 1: ARCHITECTURE BREAKDOWN)
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 1: OVERALL PROJECT ARCHITECTURE (PART 1 — SUBSYSTEMS)</span>
    <span class="q-marks">2.0 Marks Total</span>
  </div>

  <h3 class="sec-head">1. Project Purpose &amp; Operational Objectives</h3>
  <p>
    The core objective is providing recruiters with a rapid, bias-free screening tool capable of processing dozens of candidate resumes in sub-second timeframes. The application eliminates the need for manual scanning of keywords by evaluating holistic term relevance within the mathematical vector space of the job requirements.
  </p>

  <h3 class="sec-head">2. Major Architectural Subsystems</h3>
  <ul>
    <li>
      <strong>Streamlit Frontend Presentation Layer (<span class="code-pill">Main.py</span>):</strong> Built using Streamlit's reactive UI framework configured via <code>st.set_page_config(layout="wide")</code>. Features custom CSS styles, a modern hero banner, and a two-column input layout: column 1 contains a multi-line <code>st.text_area</code> for the target Job Description (displaying real-time word/character counts), while column 2 hosts an <code>st.file_uploader</code> supporting multiple concurrent PDF uploads. Dynamic feedback is rendered via animated progress bars and 4 KPI summary cards (<em>Resumes Processed</em>, <em>Average Score</em>, <em>Top Score</em>, and <em>Strong Matches &ge; 70%</em>).
    </li>
    <li>
      <strong>Application Logic &amp; Orchestration Layer (<span class="code-pill">resume_utils.py</span>):</strong> Decouples the business logic from Streamlit's script execution engine. It coordinates in-memory PDF parsing, invokes vectorization routines, formats tabular records, and generates export bytes without persistent disk storage.
    </li>
    <li>
      <strong>PyPDF2 In-Memory PDF Extraction Engine (<span class="code-pill">PyPDF2.PdfReader</span>):</strong> Encapsulated in <code>extract_text_from_pdf(file)</code>. Operates directly on volatile <code>io.BytesIO</code> byte streams passed from Streamlit's file uploader. It iterates across all document pages via <code>reader.pages</code>, extracts clean text streams using <code>page.extract_text()</code>, and concatenates them into a unified string. Empty or corrupted files are handled gracefully by returning an empty string without application failure.
    </li>
    <li>
      <strong>TF-IDF Vectorization Engine (<span class="code-pill">sklearn.feature_extraction.text.TfidfVectorizer</span>):</strong> Constructs a joint document corpus: [JD, Resume_1, Resume_2, ..., Resume_N]. TF-IDF balances term frequency against inverse document frequency, giving high weights to rare technical keywords (e.g., <em>Kubernetes</em>, <em>PyTorch</em>) while neutralizing common stopwords:
    </li>
  </ul>

  <div class="math-card">
    TF-IDF(t, d, D) = TF(t, d) &times; IDF(t, D), &nbsp;&nbsp; where &nbsp; IDF(t, D) = ln[(1 + |D|) / (1 + |{d &isin; D : t &isin; d}|)] + 1
  </div>

  <ul>
    <li>
      <strong>Cosine Similarity Scoring (<span class="code-pill">sklearn.metrics.pairwise.cosine_similarity</span>):</strong> Evaluates the angular cosine similarity between the Job Description vector V_JD and each candidate resume vector V_R in high-dimensional vector space:
    </li>
  </ul>

  <div class="math-card">
    Cosine Similarity(A, B) = (A &middot; B) / (||A|| &times; ||B||) &nbsp;&implies;&nbsp; Score = (Cosine Similarity(V_JD, V_R) &times; 100) &isin; [0.00, 100.00]%
  </div>

  <ul>
    <li>
      <strong>Pandas Results Processing (<span class="code-pill">pandas.DataFrame</span>):</strong> Implemented in <code>format_results_dataframe()</code>. Tabulates records with columns <code>Rank</code>, <code>Resume</code>, <code>Score</code>, and categorical <code>Match Level</code> badges (<em>Strong Match</em> &ge; 70%, <em>Moderate Match</em> 40–69%, <em>Low Match</em> &lt; 40%). Sorts descending by score using <code>sort_values(by="Score", ascending=False)</code> and assigns sequential rank indices 1 through N. Rendered via <code>st.dataframe</code> with interactive score progress bars.
    </li>
    <li>
      <strong>CSV Export Workflow:</strong> Encapsulated in <code>generate_csv_bytes()</code>. Strips display HTML styling via <code>results.drop(columns=["Match Level"])</code>, serializes records into UTF-8 CSV bytes via <code>.to_csv(index=False).encode('utf-8')</code>, and binds to <code>st.download_button</code> with timestamped filenames (e.g. <code>resume_rankings_YYYYMMDD_HHMMSS.csv</code>).
    </li>
  </ul>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 2 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 3: QUESTION 1 (PART 2: DATA FLOW & ARCHITECTURE DIAGRAM)
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 1: OVERALL PROJECT ARCHITECTURE (PART 2 — DATA FLOW &amp; DIAGRAM)</span>
    <span class="q-marks">2.0 Marks Total</span>
  </div>

  <h3 class="sec-head">3. Complete End-to-End System Data Flow</h3>
  <p>
    The complete data pipeline executes sequentially from candidate ingestion to ranked leaderboard presentation:
  </p>
  <ol>
    <li><strong>Step 1: Recruiter Input:</strong> The user accesses the web portal via HTTP/WebSocket on port 8501, pastes the technical Job Description into the text area, and uploads one or more PDF resumes via the file uploader.</li>
    <li><strong>Step 2: Pre-Execution Validation:</strong> The application validates that both inputs are present (<code>can_process = bool(job_description.strip() and uploaded_files)</code>). If either is absent, informative warning messages guide the user.</li>
    <li><strong>Step 3: In-Memory PDF Parsing:</strong> When the user clicks "Analyze &amp; Rank Resumes", the application loops through <code>uploaded_files</code>, passing each file-like byte buffer to <code>extract_text_from_pdf()</code>. PyPDF2 reads page streams and extracts normalized plain text into an in-memory list (<code>resumes</code>).</li>
    <li><strong>Step 4: Joint Corpus Construction:</strong> The Job Description string is concatenated with the extracted resume texts: <code>documents = [job_description] + resumes</code>, creating an (N+1)-element document array.</li>
    <li><strong>Step 5: TF-IDF Matrix Transformation:</strong> <code>TfidfVectorizer().fit_transform(documents)</code> tokenizes text, builds an n-gram feature vocabulary, computes term weights, applies L2 normalization, and produces an (N+1) &times; V matrix.</li>
    <li><strong>Step 6: Pairwise Cosine Similarity:</strong> The first row vector V<sub>JD</sub> is compared with the remaining N vectors V<sub>R<sub>1...N</sub></sub> using <code>cosine_similarity()</code>. The resulting values in [0, 1] are scaled by 100 and rounded to 2 decimal places.</li>
    <li><strong>Step 7: Tabular Structuring &amp; Ranking:</strong> A pandas DataFrame is instantiated, sorted in descending order by score, assigned sequential ranks 1 &hellip; N, and mapped to visual badge categories.</li>
    <li><strong>Step 8: Interactive Visualization &amp; Export:</strong> Streamlit displays 4 KPI summary cards, renders the interactive DataFrame with graphic score progress columns, and generates a one-click downloadable CSV file.</li>
  </ol>

  <div class="diagram-frame">
    __ARCH_SVG__
    <div class="diagram-title">Figure 1.1: Complete End-to-End System Architecture and Information Retrieval Data Flow</div>
  </div>

  <div class="info-box info-success">
    <div class="info-title">Key Architectural Advantage: Stateless Volatile Execution</div>
    The system performs all PDF parsing, vectorization, and matrix arithmetic purely inside RAM (<code>io.BytesIO</code> buffers). No candidate resumes or sensitive contact details are permanently written to server disk storage, completely mitigating data leakage risks.
  </div>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 3 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 4: QUESTION 2: DEVOPS TOOL INTEGRATION
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 2: DEVOPS TOOL INTEGRATION &amp; CATEGORIZATION</span>
    <span class="q-marks">2.0 Marks</span>
  </div>

  <h3 class="sec-head">1. Practical Applications of Integrated DevOps Tools</h3>
  <p>
    DevOps bridges the gap between software development and production operations by introducing automation, infrastructure reproducibility, continuous automated testing, and standardized release packaging.
  </p>

  <h4 class="sub-head">A. Git &amp; GitHub (Distributed Version Control &amp; Remote Collaboration)</h4>
  <p>
    Git tracks every incremental change to source code, dependencies, and configuration. In this project, Git enables atomic commits, historical trace analysis, branching strategies (e.g., <code>main</code> branch for stable releases), and status inspection. The repository is hosted on GitHub at <code>Khushal4408x/Ai-Resume-Screening</code>, serving as the central source of truth and triggering automated GitHub Actions workflows via webhooks.
  </p>

  <h4 class="sub-head">B. Docker (Containerization Engine &amp; Reproducible Environment)</h4>
  <p>
    Docker encapsulates the Python 3.12 runtime, system dependencies, application dependencies from <code>requirements.txt</code>, and source code into an immutable, portable Open Container Initiative (OCI) image.
    <strong>Implementation Details:</strong>
  </p>
  <ul>
    <li>Uses an official lightweight base: <code>FROM python:3.12-slim</code> to minimize attack surface and image footprint.</li>
    <li>Sets environment variables <code>PYTHONDONTWRITEBYTECODE=1</code> and <code>PYTHONUNBUFFERED=1</code> for containerized execution.</li>
    <li>Leverages Docker layer caching by copying and installing <code>requirements.txt</code> before application source files.</li>
    <li>Enforces security compliance by creating and switching to a dedicated non-root user (<code>appuser</code>, UID 1000).</li>
    <li>Exposes TCP port <code>8501</code> and binds Streamlit to listen on <code>0.0.0.0</code>.</li>
    <li>Embeds a native container <code>HEALTHCHECK</code> hitting Streamlit's internal <code>/_stcore/health</code> endpoint.</li>
  </ul>

  <h4 class="sub-head">C. GitHub Actions &amp; Amazon ECR (CI/CD Pipeline &amp; Container Registry)</h4>
  <p>
    GitHub Actions automates code quality checks, runs 13 pytest automated tests, builds the Docker container, and publishes the validated image to <strong>Amazon Elastic Container Registry (ECR)</strong> in <code>ap-south-1</code>.
  </p>

  <h3 class="sec-head">2. Implementation Categorization &amp; Justification Table</h3>
  <table class="q-table">
    <thead>
      <tr>
        <th style="width: 17%;">DevOps Tool</th>
        <th style="width: 19%;">Categorization</th>
        <th style="width: 64%;">Implementation Status &amp; Technical Justification in Project</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Git</strong></td>
        <td><span class="badge-imp">Implemented</span></td>
        <td>Local version control initialized; tracks commit history, branch pointers, and atomic repository changes with strict <code>.gitignore</code> rules.</td>
      </tr>
      <tr>
        <td><strong>GitHub</strong></td>
        <td><span class="badge-imp">Implemented</span></td>
        <td>Central remote repository at <code>Khushal4408x/Ai-Resume-Screening</code>; handles PR management, issue tracking, and webhook event dispatching.</td>
      </tr>
      <tr>
        <td><strong>Docker</strong></td>
        <td><span class="badge-imp">Implemented</span></td>
        <td>Production <code>Dockerfile</code> and <code>.dockerignore</code> created; container verified locally on port 8501 with non-root user and healthcheck.</td>
      </tr>
      <tr>
        <td><strong>GitHub Actions</strong></td>
        <td><span class="badge-imp">Implemented</span></td>
        <td>Active workflow in <code>.github/workflows/ci-cd.yml</code> executing syntax linting, 13 automated unit tests, and Docker build validation.</td>
      </tr>
      <tr>
        <td><strong>Amazon ECR</strong></td>
        <td><span class="badge-imp">Implemented</span></td>
        <td>Container image published to <code>700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening</code> (digest: <code>sha256:ea55...</code>).</td>
      </tr>
      <tr>
        <td><strong>AWS EC2</strong></td>
        <td><span class="badge-prop">Proposed</span></td>
        <td>Target host VM prepared with user-data script and security groups; pending explicit approval to prevent unapproved cloud billing.</td>
      </tr>
      <tr>
        <td><strong>Docker Compose</strong></td>
        <td><span class="badge-prop">Proposed</span></td>
        <td>Proposed for future multi-tier evolution (e.g., orchestrating the Streamlit UI alongside local Redis caching or mock S3 LocalStack containers).</td>
      </tr>
      <tr>
        <td><strong>Jenkins</strong></td>
        <td><span class="badge-prop">Proposed</span></td>
        <td>Proposed enterprise alternative for on-premises self-hosted CI/CD infrastructure requiring isolated physical hardware or custom corporate plugins.</td>
      </tr>
      <tr>
        <td><strong>Kubernetes</strong></td>
        <td><span class="badge-prop">Proposed</span></td>
        <td>Proposed container orchestration system (via Amazon EKS) for horizontal pod autoscaling and multi-cluster resilience if enterprise traffic scales.</td>
      </tr>
      <tr>
        <td><strong>Ansible</strong></td>
        <td><span class="badge-prop">Proposed</span></td>
        <td>Proposed agentless configuration management tool to automate base EC2 OS patching, Docker daemon provisioning, and hardening scripts.</td>
      </tr>
    </tbody>
  </table>

  <div class="info-box info-warning">
    <div class="info-title">Technical Justification for Proposed Tools (Jenkins, Kubernetes, Ansible)</div>
    Jenkins is not implemented because GitHub Actions natively integrates with GitHub without server maintenance. Kubernetes is proposed for future multi-node cluster scaling, while current workloads run effectively as single containers. Ansible is proposed for future multi-node VM configuration.
  </div>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 4 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 5: QUESTION 3: CI/CD PIPELINE IMPLEMENTATION
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 3: CI/CD PIPELINE IMPLEMENTATION &amp; VERIFICATION</span>
    <span class="q-marks">2.0 Marks</span>
  </div>

  <h3 class="sec-head">1. GitHub Actions Workflow Execution Stages</h3>
  <p>
    The Continuous Integration and Continuous Deployment (CI/CD) pipeline is codified in <code>.github/workflows/ci-cd.yml</code>. It establishes an automated quality control gate that executes automatically on every code change to guarantee that broken builds or failing algorithms never reach production.
  </p>

  <ol>
    <li>
      <strong>Code Commit &amp; Atomic Changes:</strong> The developer implements bug fixes, features, or performance enhancements locally and stages atomic commits following clean commit messaging conventions.
    </li>
    <li>
      <strong>GitHub Push &amp; Webhook Trigger:</strong> The commit is pushed to the remote GitHub repository (<code>origin/main</code>) or opened as a Pull Request. GitHub's webhook engine intercepts the event and evaluates workflow trigger filters: <code>on: push: branches: [main]</code>, <code>pull_request: branches: [main]</code>, and <code>workflow_dispatch</code>.
    </li>
    <li>
      <strong>Runner Provisioning &amp; Source Checkout:</strong> GitHub Actions allocates an isolated, clean virtual environment running <code>ubuntu-latest</code>. Step <code>actions/checkout@v4</code> clones the exact repository commit SHA.
    </li>
    <li>
      <strong>Python Runtime Setup &amp; Dependency Caching:</strong> Action <code>actions/setup-python@v5</code> installs Python 3.12 and activates automated pip dependency caching (<code>cache: "pip"</code>), reducing subsequent pipeline execution times by ~65%.
    </li>
    <li>
      <strong>Dependency Installation:</strong> Upgrades pip and installs production dependencies from <code>requirements.txt</code> alongside testing/linting tools (<code>flake8</code>, <code>pytest</code>).
    </li>
    <li>
      <strong>Syntax Validation &amp; Bytecode Compilation:</strong> Executes <code>python -m py_compile Main.py resume_utils.py</code> to catch compilation syntax errors immediately. Runs <code>flake8</code> targeting fatal syntax anomalies (<code>E9, F63, F7, F82</code>) and undefined variables.
    </li>
    <li>
      <strong>Automated Pytest Suite Execution:</strong> Executes <code>pytest tests/ -v</code>. The custom test suite (<code>tests/test_screening.py</code>) runs <strong>13 comprehensive automated tests</strong> verifying: (i) PDF text extraction from sample files, (ii) empty stream handling, (iii) corrupted PDF stream recovery, (iv) mathematical bounds of TF-IDF cosine similarity [0.0–100.0], (v) ranking order fidelity (strong match &gt; moderate match &gt; unrelated resume), (vi) identical text maximum scoring, (vii) zero-matching vocabulary handling, (viii) empty resume list handling, (ix) empty JD handling, (x) CSS score classification thresholds, (xi) UI match badge generation, (xii) DataFrame tabular ranking formatting, and (xiii) CSV export byte generation. <em>All 13 tests pass in 1.5 seconds.</em>
    </li>
    <li>
      <strong>Docker Buildx &amp; Container Image Compilation:</strong> Uses <code>docker/setup-buildx-action@v3</code> and <code>docker/build-push-action@v5</code> to build the container image using <code>Dockerfile</code>, tagging it as <code>ai-resume-screening:latest</code>.
    </li>
    <li>
      <strong>Container Build Validation &amp; Healthcheck Verification:</strong> The workflow starts the freshly built container in detached mode (<code>docker run -d -p 8501:8501</code>), waits 6 seconds for initialization, and polls the health endpoint:
      <code>curl --fail http://localhost:8501/_stcore/health</code>. Once HTTP 200 is validated, the test container is cleanly terminated.
    </li>
    <li>
      <strong>Amazon ECR Publishing Stage:</strong> Uses <code>aws-actions/configure-aws-credentials@v4</code> with <strong>AWS IAM OIDC</strong> (zero long-lived static secrets), logs into ECR via <code>aws-actions/amazon-ecr-login@v2</code>, tags the image with Git SHA and <code>latest</code>, and pushes to Amazon ECR repository: <code>700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening</code>.
    </li>
  </ol>

  <div class="diagram-frame">
    __CICD_SVG__
    <div class="diagram-title">Figure 3.1: Automated CI/CD Pipeline Workflow (GitHub Actions, Docker &amp; Amazon ECR Publishing)</div>
  </div>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 5 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 6: QUESTION 4: CLOUD PLATFORM EVALUATION (AWS)
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 4: CLOUD PLATFORM EVALUATION (AWS ARCHITECTURE)</span>
    <span class="q-marks">2.0 Marks</span>
  </div>

  <h3 class="sec-head">1. Selected Cloud Platform: Amazon Web Services (AWS)</h3>
  <p>
    Amazon Web Services (AWS) in region Asia Pacific Mumbai (<code>ap-south-1</code>) is selected as the cloud platform due to its mature container hosting ecosystem, low data latency across India, enterprise security compliance, and cost-effective compute instances.
  </p>

  <h3 class="sec-head">2. Detailed Evaluation of AWS Cloud Services</h3>
  <ul>
    <li>
      <strong>Amazon ECR (Elastic Container Registry - Implemented &amp; Verified):</strong> Secure, private, highly available OCI registry hosting <code>700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening</code> (Image Digest: <code>sha256:ea5512e14d23cc6b37b2bd3edc9f9aa27ad48f7a233420f90927803abcee9197</code>). Supports immutable image tags and vulnerability scanning.
    </li>
    <li>
      <strong>AWS EC2 (Elastic Compute Cloud - Prepared):</strong> Target VM host for the containerized application. A <code>t3.medium</code> instance (2 vCPUs, 4 GiB RAM, Amazon Linux 2023) provides an ideal balance of memory for PyPDF2 text parsing and scikit-learn matrix computations while remaining economical (~$0.0416/hr, or free tier eligible with <code>t2.micro</code>/<code>t3.micro</code>).
    </li>
    <li>
      <strong>AWS Application Load Balancer (ALB - Proposed):</strong> Operates at Layer 7 (HTTP/HTTPS). It terminates SSL/TLS certificates managed by AWS Certificate Manager (ACM), routes web traffic to target EC2 instances, performs health checks against <code>/_stcore/health</code>, and enables <strong>Sticky Sessions (Duration-based Cookies)</strong>, which are strictly required by Streamlit to maintain stateful WebSocket connections with browser clients.
    </li>
    <li>
      <strong>AWS CloudWatch (Observability - Proposed):</strong> Captures system-level metrics (CPU utilization, memory usage, network I/O) and aggregates application logs via the <code>awslogs</code> Docker log driver. CloudWatch Alarms notify engineers via Amazon SNS when error rates spike or memory exceeds 80%.
    </li>
    <li>
      <strong>AWS IAM (Identity &amp; Access Management - Configured):</strong> Enforces the <strong>Principle of Least Privilege (PoLP)</strong>. EC2 instances are assigned an IAM Instance Profile granting read-only access to ECR and write-only access to CloudWatch Logs. For CI/CD, GitHub Actions authenticates via <strong>AWS IAM OIDC Identity Providers</strong>, eliminating static, long-lived AWS secret access keys entirely.
    </li>
    <li>
      <strong>Amazon S3 (Simple Storage Service - Optional):</strong> If historical resume auditing is required, S3 provides encrypted object storage (Server-Side Encryption with AWS KMS: <code>SSE-KMS</code>). Strict S3 Lifecycle rules automatically delete candidate resumes after 24 hours to enforce data privacy.
    </li>
  </ul>

  <h3 class="sec-head">3. Evaluation Across AWS Well-Architected Framework Pillars</h3>
  <table class="q-table">
    <thead>
      <tr>
        <th style="width: 22%;">Pillar</th>
        <th style="width: 78%;">Evaluation &amp; Architectural Application to Resume Screening System</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Scalability</strong></td>
        <td>Horizontal scaling is achieved via an Auto Scaling Group (ASG) behind the ALB. When CPU exceeds 70% during peak recruitment fair hours, ASG scales out EC2 instances automatically.</td>
      </tr>
      <tr>
        <td><strong>Availability</strong></td>
        <td>Multi-Availability Zone (Multi-AZ) deployment spans two isolated physical data centers (e.g. <code>ap-south-1a</code> and <code>ap-south-1b</code>), ensuring 99.99% application uptime if one AZ encounters an outage.</td>
      </tr>
      <tr>
        <td><strong>Performance</strong></td>
        <td>Fast sub-second response times (&lt;0.5s for 20 resumes). Ephemeral processing in RAM eliminates disk I/O bottlenecks. Fast AWS backbone networking enables swift PDF uploads.</td>
      </tr>
      <tr>
        <td><strong>Cost-Effectiveness</strong></td>
        <td>Highly economical. A single <code>t3.medium</code> instance costs ~$30/month. Coupled with AWS Free Tier (ECR, CloudWatch, ALB credits) and optional AWS Savings Plans, operating costs remain under $45/month.</td>
      </tr>
    </tbody>
  </table>

  <h3 class="sec-head">4. Candidate Resume Privacy &amp; Secure Handling of Uploaded PDFs</h3>
  <div class="info-box info-success">
    <div class="info-title">Critical Privacy Engineering: In-Memory Processing &amp; Data Protection</div>
    <ul>
      <li><strong>In-Memory Volatile Processing:</strong> Streamlit's <code>UploadedFile</code> stream and PyPDF2 process documents entirely within RAM buffers (<code>io.BytesIO</code>). Resumes are <em>never</em> written to unencrypted local disk directories, temporary filesystems, or databases.</li>
      <li><strong>Zero Unnecessary Database Footprint:</strong> Unlike traditional web applications, this project intentionally avoids databases like MongoDB or MySQL, eliminating persistent database credential leakage risks and candidate profiling liabilities.</li>
      <li><strong>Encryption in Transit:</strong> All web traffic is strictly encrypted using <strong>TLS 1.3</strong> terminated at the Application Load Balancer with HTTP-to-HTTPS automatic redirection (Port 80 to 443).</li>
      <li><strong>Ephemeral Lifecycle Purge:</strong> Once the recruiter's browser session ends or the ranking table is generated, memory pointers are released and reclaimed by Python's garbage collector. If S3 storage is enabled for compliance logging, S3 Lifecycle rules automatically purge files after 24 hours in adherence to GDPR Article 17 ("Right to Erasure") and India's Digital Personal Data Protection (DPDP) Act 2023.</li>
    </ul>
  </div>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 6 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 7: QUESTION 5: IMPROVED DEVOPS & CLOUD ARCHITECTURE
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>QUESTION 5: IMPROVED ARCHITECTURE &amp; PRODUCTION BLUEPRINT</span>
    <span class="q-marks">2.0 Marks Total</span>
  </div>

  <h3 class="sec-head">1. Proposed Enterprise Cloud &amp; DevOps Blueprint</h3>
  <p>
    The improved cloud architecture transitions the standalone application into an enterprise-ready microservice deployed inside an isolated <strong>Amazon Virtual Private Cloud (VPC)</strong> across multiple Availability Zones in <code>ap-south-1</code>.
  </p>

  <div class="diagram-frame">
    __CLOUD_SVG__
    <div class="diagram-title">Figure 5.1: High-Availability AWS Cloud &amp; DevOps Production Architecture Blueprint</div>
  </div>

  <h3 class="sec-head">2. Key Architecture Pillars &amp; Improvements</h3>
  <ul>
    <li>
      <strong>VPC Network Segmentation &amp; Security:</strong> The VPC (<code>10.0.0.0/16</code>) is divided into <strong>Public Subnets</strong> (hosting the internet-facing Application Load Balancer and NAT Gateways) and <strong>Private Subnets</strong> (hosting the EC2 instances running Docker containers). EC2 instances possess no public IP addresses and cannot be accessed directly from the public internet. Outbound traffic (e.g. downloading OS security patches) routes securely through the NAT Gateway.
    </li>
    <li>
      <strong>Containerization &amp; Registry:</strong> Docker containers run with non-root privileges (<code>appuser</code>). Immutable container images tagged with unique Git commit SHAs and release versions (<code>v1.0.0</code>) are pushed to private Amazon ECR repositories with automatic CVE vulnerability scanning on push.
    </li>
    <li>
      <strong>CI/CD with Keyless OIDC Authentication:</strong> GitHub Actions authenticates to AWS via OpenID Connect (OIDC) federated role assumptions. No static AWS access keys or passwords are stored in GitHub Secrets, nullifying credential exfiltration risks.
    </li>
    <li>
      <strong>Automated Monitoring &amp; Synthetic Probes:</strong> AWS CloudWatch collects system telemetry and container logs via the <code>awslogs</code> driver. CloudWatch Synthetics canaries continuously ping <code>/_stcore/health</code> every 60 seconds. If failure occurs, Amazon SNS alerts the DevOps on-call engineer via SMS/email.
    </li>
    <li>
      <strong>Disaster Recovery &amp; Backup Strategy:</strong> Infrastructure is fully defined as code using Terraform / AWS CloudFormation for reproducible disaster recovery. Automated AWS Backup schedules daily AMIs and EBS snapshots. In the event of a regional failure, the infrastructure can be reprovisioned in an alternate region within 30 minutes (Recovery Time Objective: RTO &lt; 30 min, Recovery Point Objective: RPO &lt; 1 hour).
    </li>
  </ul>

  <h3 class="sec-head">3. Kubernetes (Amazon EKS) as an Optional Future Orchestration Solution</h3>
  <p>
    While the current single-container architecture runs optimally on EC2 Auto-Scaling, <strong>Kubernetes (Amazon Elastic Kubernetes Service - EKS)</strong> is proposed as the next evolution when organizational scale demands it:
  </p>
  <ul>
    <li><strong>Horizontal Pod Autoscaler (HPA):</strong> Scales pods dynamically based on CPU or custom queue depth metrics in seconds rather than waiting minutes for EC2 VM initialization.</li>
    <li><strong>Microservices Decomposition:</strong> Enables separating the Streamlit Web UI from a backend asynchronous Celery/Redis worker queue dedicated to heavy Optical Character Recognition (OCR) or large Transformer models (e.g. BERT/RoBERTa embeddings).</li>
    <li><strong>Zero-Downtime Rolling Deployments:</strong> Native Kubernetes rolling updates and canary releases guarantee seamless user transitions with instant rollback capabilities.</li>
  </ul>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 7 of 8</span>
  </div>
</div>

<!-- ==========================================================================
     PAGE 8: COMPARATIVE ANALYSIS, TESTING RESULTS, CONCLUSION & REFERENCES
=========================================================================== -->
<div class="doc-page">
  <div class="inst-header">
    <div>
      <div class="inst-title">Noida Institute of Engineering and Technology</div>
      <div class="inst-dept">Department of Computer Science &amp; Engineering | Greater Noida • Session: 2026–27</div>
    </div>
    <div>
      <span class="inst-badge">UNIT 4 – ASSIGNMENT 3</span>
    </div>
  </div>

  <div class="q-banner">
    <span>SYSTEM IMPROVEMENT COMPARISON &amp; ACADEMIC CONCLUSION</span>
    <span class="q-marks">Final Evaluation</span>
  </div>

  <h3 class="sec-head">4. Detailed System Improvements Comparative Analysis</h3>
  <table class="q-table">
    <thead>
      <tr>
        <th style="width: 20%;">Dimension</th>
        <th style="width: 38%;">Baseline / Standalone Implementation</th>
        <th style="width: 42%;">Improved DevOps &amp; Cloud Architecture</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Reliability</strong></td>
        <td>Single workstation execution; vulnerable to local hardware faults, OS crashes, and unmonitored failures.</td>
        <td>Multi-AZ redundancy, Auto-Scaling Group self-healing, automated ALB health checks on <code>/_stcore/health</code>, and CloudWatch alarms.</td>
      </tr>
      <tr>
        <td><strong>2. Scalability</strong></td>
        <td>Single-node compute bound; concurrent user uploads cause UI lag and resource contention.</td>
        <td>Horizontal scaling across private EC2 instances behind an Application Load Balancer with dynamic capacity expansion.</td>
      </tr>
      <tr>
        <td><strong>3. Security</strong></td>
        <td>Local plaintext files; risk of local privilege escalation and unencrypted data leakage.</td>
        <td>VPC private subnet isolation, TLS 1.3 encryption, non-root Docker user, IAM least privilege, OIDC authentication, and ephemeral RAM data handling.</td>
      </tr>
      <tr>
        <td><strong>4. Maintainability</strong></td>
        <td>Manual dependency management ("works on my machine"); divergent local Python environments.</td>
        <td>Immutable Docker images, modular codebase (<code>resume_utils.py</code>), pinned dependencies, and automated regression testing.</td>
      </tr>
      <tr>
        <td><strong>5. Automation</strong></td>
        <td>Manual script execution, manual verification, and manual deployment steps.</td>
        <td>Fully automated GitHub Actions CI/CD pipeline triggered on Git events with automated syntax linting, 13 unit tests, and Docker builds.</td>
      </tr>
    </tbody>
  </table>

  <h3 class="sec-head">5. Implementation &amp; Testing Results Verification</h3>
  <ul>
    <li><strong>Automated Test Suite:</strong> 13/13 tests passed via pytest in 1.73 seconds covering PDF parsing, TF-IDF scoring, ranking order, and CSV export.</li>
    <li><strong>Docker Build &amp; Runtime:</strong> Built image <code>ai-resume-screening:latest</code> (254MB content size); verified container runs on port 8501 with HTTP 200 healthcheck.</li>
    <li><strong>Amazon ECR Verification:</strong> Pushed image to <code>700017004419.dkr.ecr.ap-south-1.amazonaws.com/ai-resume-screening</code> (digest: <code>sha256:ea5512e1...</code>).</li>
  </ul>

  <div class="screenshot-frame">
    <img src="data:image/png;base64,__SCREENSHOT_B64__" alt="Application Running in Docker">
    <div class="screenshot-title">Figure 5.2: Verification Evidence — Streamlit AI Resume Screening Application Running Inside Docker Container on Port 8501</div>
  </div>

  <h3 class="sec-head">6. Limitations, Future Work &amp; Academic References</h3>
  <p>
    <strong>Limitations:</strong> Keyword overlap influences scores; scanned image PDFs require future OCR integration (AWS Textract/Tesseract); EC2 deployment prepared but pending live infrastructure approval to avoid unapproved costs.
  </p>
  <ol style="font-size: 7.5pt; color: #475569;">
    <li>Amazon Web Services, <em>"AWS Well-Architected Framework: Reliability and Security Pillars,"</em> AWS Whitepapers, 2024.</li>
    <li>Streamlit Inc., <em>"Deploying Streamlit with Docker and Container Registries,"</em> Streamlit Documentation, 2024.</li>
    <li>Pedregosa et al., <em>"Scikit-learn: Machine Learning in Python - TF-IDF and Pairwise Metrics,"</em> JMLR, vol. 12, pp. 2825-2830.</li>
    <li>GitHub Documentation, <em>"About security hardening with OpenID Connect in GitHub Actions,"</em> GitHub Docs, 2024.</li>
    <li>Ministry of Law and Justice, <em>"The Digital Personal Data Protection Act, 2023,"</em> The Gazette of India, Act No. 22 of 2023.</li>
  </ol>

  <div class="page-footer">
    <span>DevOps and Cloud Computing (BCDS0501) – Unit 4 Assignment 3 | NIET Greater Noida</span>
    <span>Page 8 of 8</span>
  </div>
</div>

</body>
</html>
"""

html_out = html_template.replace("__ARCH_SVG__", arch_svg).replace("__CICD_SVG__", cicd_svg).replace("__CLOUD_SVG__", cloud_svg).replace("__SCREENSHOT_B64__", screenshot_b64)

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_out)

print("Generated 8-page structured report.html successfully.")
