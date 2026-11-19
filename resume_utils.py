"""
resume_utils.py - Core processing functions for AI-Powered Resume Screening and Ranking System.
Provides modular, testable logic for PDF text extraction, TF-IDF cosine similarity ranking,
and tabular result formatting for Streamlit presentation and CSV export.
"""

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


def extract_text_from_pdf(file):
    """
    Extract readable text from all pages of an uploaded PDF file object.
    Gracefully handles empty or corrupted files by returning an empty string.
    
    Args:
        file: A file-like object or file path containing the PDF document.
        
    Returns:
        str: Concatenated text extracted from all pages of the PDF.
    """
    try:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception:
        return ""


def rank_resumes(job_description, resumes):
    """
    Rank resumes based on TF-IDF representation and cosine similarity against a job description.
    
    Args:
        job_description (str): Target job description text.
        resumes (list of str): List of extracted resume texts.
        
    Returns:
        numpy.ndarray: Array of percentage similarity scores rounded to 2 decimal places.
    """
    if not resumes or not job_description.strip():
        return np.array([])
        
    documents = [job_description] + resumes
    try:
        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        job_description_vector = vectors[0]
        resume_vectors = vectors[1:]
        cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

        scores = (cosine_similarities * 100).round(2)
        return scores
    except ValueError:
        # Handle cases with empty vocabulary
        return np.zeros(len(resumes), dtype=float)


def get_score_class(score):
    """
    Return CSS class name based on candidate match score threshold.
    """
    if score >= 70:
        return "score-high"
    elif score >= 40:
        return "score-medium"
    return "score-low"


def get_badge(score):
    """
    Return HTML badge representation based on match score threshold.
    """
    if score >= 70:
        return '<span class="badge badge-success">Strong Match</span>'
    elif score >= 40:
        return '<span class="badge badge-warning">Moderate Match</span>'
    return '<span class="badge badge-info">Low Match</span>'


def format_results_dataframe(file_names, scores):
    """
    Construct, sort, and rank candidate DataFrame descending by score.
    
    Args:
        file_names (list of str): Names of the resume files.
        scores (list or np.ndarray): Similarity scores corresponding to each resume.
        
    Returns:
        pd.DataFrame: Formatted DataFrame with Rank, Resume, Score, and Match Level.
    """
    if not file_names or len(file_names) != len(scores):
        return pd.DataFrame(columns=["Rank", "Resume", "Score", "Match Level"])

    results = pd.DataFrame({
        "Rank": range(1, len(file_names) + 1),
        "Resume": list(file_names),
        "Score": scores,
        "Match Level": [get_badge(s) for s in scores]
    }).sort_values(by="Score", ascending=False).reset_index(drop=True)

    results["Rank"] = range(1, len(results) + 1)
    return results


def generate_csv_bytes(results_df):
    """
    Export results DataFrame as clean UTF-8 CSV bytes excluding display HTML badges.
    
    Args:
        results_df (pd.DataFrame): DataFrame containing ranking results.
        
    Returns:
        bytes: Encoded CSV byte representation.
    """
    if results_df.empty:
        return b""
    df_clean = results_df.drop(columns=["Match Level"]) if "Match Level" in results_df.columns else results_df
    return df_clean.to_csv(index=False).encode('utf-8')
