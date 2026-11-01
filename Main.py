import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# Page configuration
st.set_page_config(
    page_title="AI Resume Screening & Ranking",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional, clean, modern UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #2563eb;
        --primary-hover: #1d4ed8;
        --primary-light: #dbeafe;
        --secondary: #64748b;
        --success: #059669;
        --success-light: #d1fae5;
        --warning: #d97706;
        --danger: #dc2626;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --radius: 8px;
        --radius-lg: 12px;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero section */
    .hero {
        background: linear-gradient(135deg, var(--primary) 0%, #1e40af 100%);
        border-radius: var(--radius-lg);
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: var(--shadow-md);
    }
    .hero h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .hero p {
        margin: 0;
        font-size: 1.125rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Section cards */
    .section-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 0.2s, border-color 0.2s;
    }
    .section-card:hover {
        box-shadow: var(--shadow);
        border-color: var(--primary-light);
    }
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    .section-icon {
        width: 24px;
        height: 24px;
        color: var(--primary);
    }

    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed var(--border);
        border-radius: var(--radius);
        padding: 2rem;
        background: var(--bg-secondary);
        transition: all 0.2s;
    }
    .stFileUploader > div > div:hover {
        border-color: var(--primary);
        background: var(--primary-light);
    }
    .stFileUploader label {
        font-weight: 500;
        color: var(--text-primary);
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        background: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9375rem;
        line-height: 1.6;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-light);
    }

    /* Button styling */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        width: 100%;
        transition: all 0.2s;
        box-shadow: var(--shadow-sm);
    }
    .stButton > button:hover {
        background: var(--primary-hover);
        box-shadow: var(--shadow);
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stButton > button:disabled {
        background: var(--text-muted);
        cursor: not-allowed;
        transform: none;
    }

    /* Results table styling */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border-radius: var(--radius);
    }

    /* Metric cards */
    .metric-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s;
    }
    .metric-card:hover {
        box-shadow: var(--shadow);
        border-color: var(--primary-light);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
    }
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Status badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-success {
        background: var(--success-light);
        color: var(--success);
    }
    .badge-warning {
        background: #fef3c7;
        color: var(--warning);
    }
    .badge-info {
        background: var(--primary-light);
        color: var(--primary);
    }

    /* Progress bar */
    .progress-container {
        margin-top: 1rem;
    }
    .progress-bar {
        height: 6px;
        background: var(--bg-tertiary);
        border-radius: 3px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), #3b82f6);
        border-radius: 3px;
        transition: width 0.5s ease-out;
    }

    /* Score bars in results */
    .score-bar {
        height: 8px;
        background: var(--bg-tertiary);
        border-radius: 4px;
        overflow: hidden;
    }
    .score-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease-out;
    }
    .score-high { background: linear-gradient(90deg, var(--success), #34d399); }
    .score-medium { background: linear-gradient(90deg, var(--warning), #fbbf24); }
    .score-low { background: linear-gradient(90deg, var(--danger), #f87171); }

    /* Info boxes */
    .info-box {
        background: var(--primary-light);
        border: 1px solid #bfdbfe;
        border-radius: var(--radius);
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box-title {
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    .info-box ul {
        margin: 0;
        padding-left: 1.25rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    .info-box li {
        margin-bottom: 0.25rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        font-size: 0.875rem;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.4s ease-out forwards;
    }
    .delay-1 { animation-delay: 0.1s; opacity: 0; }
    .delay-2 { animation-delay: 0.2s; opacity: 0; }
    .delay-3 { animation-delay: 0.3s; opacity: 0; }

    /* Responsive */
    @media (max-width: 768px) {
        .hero h1 { font-size: 1.75rem; }
        .hero p { font-size: 1rem; }
        .main .block-container { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)


# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

    scores = (cosine_similarities * 100).round(2)
    return scores


def get_score_class(score):
    if score >= 70:
        return "score-high"
    elif score >= 40:
        return "score-medium"
    return "score-low"


def get_badge(score):
    if score >= 70:
        return '<span class="badge badge-success">Strong Match</span>'
    elif score >= 40:
        return '<span class="badge badge-warning">Moderate Match</span>'
    return '<span class="badge badge-info">Low Match</span>'


# ---- HERO SECTION ----
st.markdown("""
<div class="hero animate-in">
    <h1>📄 AI Resume Screening & Ranking</h1>
    <p>Intelligently match candidates to job descriptions using TF-IDF vectorization and cosine similarity. Upload resumes, get ranked results instantly.</p>
</div>
""", unsafe_allow_html=True)

# ---- INPUT SECTIONS ----
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="section-card animate-in delay-1">
        <div class="section-title">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <span>Job Description</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "",
        placeholder="Paste the job description here...\n\nExample:\n- 3+ years Python experience\n- Strong knowledge of ML/AI\n- Experience with TensorFlow/PyTorch\n- AWS cloud deployment skills\n- Bachelor's in CS or related field",
        height=280,
        label_visibility="collapsed",
        help="Enter the complete job description including requirements, responsibilities, and preferred qualifications."
    )

    # Character count
    if job_description:
        char_count = len(job_description)
        word_count = len(job_description.split())
        st.caption(f"{char_count:,} characters • {word_count:,} words")

with col2:
    st.markdown("""
    <div class="section-card animate-in delay-1">
        <div class="section-title">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            <span>Upload Resumes</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Upload one or more PDF resumes. Maximum 50MB per file."
    )

    if uploaded_files:
        st.markdown(f"""
        <div class="info-box">
            <div class="info-box-title">✅ {len(uploaded_files)} file(s) ready</div>
            <ul>
                {''.join(f'<li>{f.name} ({f.size / 1024:.1f} KB)</li>' for f in uploaded_files)}
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---- PROCESS BUTTON ----
st.markdown("<br>", unsafe_allow_html=True)

can_process = bool(job_description.strip() and uploaded_files)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    process_clicked = st.button(
        "🔍 Analyze & Rank Resumes",
        type="primary",
        disabled=not can_process,
        use_container_width=True
    )

if not can_process and (job_description or uploaded_files):
    missing = []
    if not job_description.strip():
        missing.append("job description")
    if not uploaded_files:
        missing.append("resume files")
    st.warning(f"⚠️ Please provide: {', '.join(missing)} to proceed.")

# ---- RESULTS SECTION ----
if process_clicked and can_process:
    with st.spinner(""):
        progress_placeholder = st.empty()
        progress_placeholder.markdown("""
        <div class="progress-container animate-in">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary); font-size: 0.875rem;">Processing resumes...</span>
                <span id="progress-pct" style="color: var(--primary); font-weight: 600;">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 0%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Simulate progress for better UX
        resumes = []
        for i, file in enumerate(uploaded_files):
            progress = int((i + 1) / len(uploaded_files) * 50)
            progress_placeholder.markdown(f"""
            <div class="progress-container animate-in">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: var(--text-secondary); font-size: 0.875rem;">Extracting text from {file.name}...</span>
                    <span style="color: var(--primary); font-weight: 600;">{progress}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            text = extract_text_from_pdf(file)
            resumes.append(text)
            time.sleep(0.1)  # Small delay for visual feedback

        progress_placeholder.markdown("""
        <div class="progress-container animate-in">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--text-secondary); font-size: 0.875rem;">Computing similarity scores...</span>
                <span style="color: var(--primary); font-weight: 600;">75%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 75%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        scores = rank_resumes(job_description, resumes)

        time.sleep(0.3)
        progress_placeholder.empty()

    # ---- METRICS ROW ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card animate-in">
        <div class="section-title">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <span>Results Summary</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown(f"""
        <div class="metric-card animate-in delay-1">
            <div class="metric-value">{len(uploaded_files)}</div>
            <div class="metric-label">Resumes Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        avg_score = scores.mean()
        st.markdown(f"""
        <div class="metric-card animate-in delay-2">
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-label">Average Score</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol3:
        top_score = scores.max()
        st.markdown(f"""
        <div class="metric-card animate-in delay-3">
            <div class="metric-value">{top_score:.1f}</div>
            <div class="metric-label">Top Score</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol4:
        strong_matches = (scores >= 70).sum()
        st.markdown(f"""
        <div class="metric-card animate-in" style="animation-delay: 0.4s; opacity: 0;">
            <div class="metric-value">{strong_matches}</div>
            <div class="metric-label">Strong Matches (≥70)</div>
        </div>
        """, unsafe_allow_html=True)

    # ---- DETAILED RESULTS ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card animate-in">
        <div class="section-title">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            <span>Detailed Rankings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create results dataframe with enhanced display
    results = pd.DataFrame({
        "Rank": range(1, len(uploaded_files) + 1),
        "Resume": [f.name for f in uploaded_files],
        "Score": scores,
        "Match Level": [get_badge(s) for s in scores]
    }).sort_values(by="Score", ascending=False).reset_index(drop=True)

    results["Rank"] = range(1, len(results) + 1)

    # Display as styled dataframe
    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("🏆 Rank", width="small"),
            "Resume": st.column_config.TextColumn("📄 Resume", width="large"),
            "Score": st.column_config.ProgressColumn(
                "📊 Score (0-100)",
                min_value=0,
                max_value=100,
                format="%.1f",
                width="medium"
            ),
            "Match Level": st.column_config.TextColumn("🎯 Match", width="medium"),
        }
    )

    # ---- DOWNLOAD RESULTS ----
    st.markdown("<br>", unsafe_allow_html=True)
    csv = results.drop(columns=["Match Level"]).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"resume_rankings_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Success message
    st.success(f"✅ Analysis complete! Processed {len(uploaded_files)} resumes in under a second.", icon="✅")

# ---- FOOTER ----
st.markdown("""
<div class="footer">
    <p>Built with Streamlit • Powered by scikit-learn TF-IDF & Cosine Similarity</p>
    <p style="margin-top: 0.5rem;">For educational and decision-support purposes only. Scores indicate textual similarity, not comprehensive candidate assessment.</p>
</div>
""", unsafe_allow_html=True)