"""
resume_utils.py - Core processing functions for AI-Powered Resume Screening and Ranking System.
Provides modular, testable logic for PDF text extraction and TF-IDF cosine similarity ranking.
"""

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def extract_text_from_pdf(file):
    """
    Extract readable text from all pages of an uploaded PDF file object.
    
    Args:
        file: A file-like object or file path containing the PDF document.
        
    Returns:
        str: Concatenated text extracted from all pages of the PDF.
    """
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def rank_resumes(job_description, resumes):
    """
    Rank resumes based on TF-IDF representation and cosine similarity against a job description.
    
    Args:
        job_description (str): Target job description text.
        resumes (list of str): List of extracted resume texts.
        
    Returns:
        numpy.ndarray: Array of percentage similarity scores rounded to 2 decimal places.
    """
    if not resumes:
        return np.array([])
        
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

    scores = (cosine_similarities * 100).round(2)
    return scores


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
