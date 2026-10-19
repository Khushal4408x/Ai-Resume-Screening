# AI-Powered Resume Screening and Ranking System

A web-based application that analyzes resumes against a job description and ranks candidates using TF-IDF vectorization and cosine similarity. Built with Python and Streamlit, this project provides a simple interface for comparing multiple PDF resumes efficiently.

## 📑 Project Documentation

For a detailed overview of the project, refer to the project document:

## 🚀 Features

- **Resume Screening:** Extract text from PDF resumes and compare it with a job description.
- **Candidate Ranking:** Rank resumes according to their textual similarity to the job description.
- **PDF Support:** Upload multiple PDF resumes for processing.
- **Similarity Scores:** Display scores on a scale of 0–100.
- **Interactive Interface:** Enter job descriptions, upload resumes, and view ranked results through Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| PyPDF2 | PDF text extraction |
| pandas | Candidate ranking and results display |
| scikit-learn | TF-IDF vectorization and cosine similarity |

## 📂 Project Structure

```text
Ai-Resume-Screening/
├── Main.py
├── README.md
├── requirements.txt
└── AI-powered-Resume-Screening-and-Ranking-System.pdf
```

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.10 or later, subject to dependency compatibility
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Khushal-beep1/Ai-Resume-Screening.git
cd Ai-Resume-Screening
```

### 2. Create a Virtual Environment

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run Main.py
```

### 5. Open the Application

Streamlit will display a local URL in your terminal, usually:

```text
http://localhost:8501
```

Open this URL in your browser to start screening resumes.

## 🔍 How It Works

1. Enter the job description in the application.
2. Upload one or more PDF resumes.
3. The application extracts text from each resume.
4. TF-IDF converts the job description and resumes into numerical text representations.
5. Cosine similarity measures the similarity between the job description and each resume.
6. The application displays the candidates ranked by similarity score.

## 🧩 Key Functions

### `extract_text_from_pdf(file)`

Extracts readable text from the pages of an uploaded PDF resume using PyPDF2.

### `rank_resumes(job_description, resumes)`

Uses `TfidfVectorizer` to represent the job description and resumes as TF-IDF vectors, then calculates cosine similarity to generate scores and rank candidates.

## ⚠️ Limitations

- The ranking is based on textual similarity, not a comprehensive assessment of a candidate's qualifications.
- Keyword overlap can influence scores, even when a resume does not demonstrate the required skills.
- Scanned PDFs may not work correctly because OCR is not currently implemented.
- Results should support human review rather than determine hiring decisions automatically.

## 🔮 Future Enhancements

- Support additional file formats, such as DOCX.
- Add OCR support for scanned resumes.
- Extract skills and identify missing job requirements.
- Provide explanations for candidate scores.
- Improve ranking with more advanced NLP techniques.
- Add candidate filtering, export options, and a more detailed results dashboard.

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch to your fork.
5. Open a pull request describing your changes.

## 📄 License

No license has been specified yet. Add a license file if you intend to define permissions for using, modifying, and distributing this project.

---

**Disclaimer:** This project is intended for educational and decision-support purposes. Resume similarity scores should not be treated as definitive measures of candidate suitability.
