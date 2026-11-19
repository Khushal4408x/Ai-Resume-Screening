"""
tests/test_screening.py - Automated test suite for AI Resume Screening System using pytest.
Covers:
- PDF text extraction from physical samples and in-memory streams.
- Empty and invalid/corrupted PDF handling.
- Resume text preprocessing and tokenization.
- TF-IDF vectorization and cosine similarity scoring.
- Candidate ranking order and accuracy.
- Similarity score validity ([0.0, 100.0] bounds).
- CSV export formatting and cleanliness.
"""

import pytest
import os
import io
import numpy as np
import pandas as pd
from resume_utils import (
    extract_text_from_pdf,
    rank_resumes,
    get_score_class,
    get_badge,
    format_results_dataframe,
    generate_csv_bytes
)


@pytest.fixture
def sample_data():
    """Provides reusable test fixtures for JD and diverse candidate resumes."""
    return {
        "jd": (
            "Senior Python Developer with expertise in Machine Learning, "
            "scikit-learn, pandas, numpy, and AWS cloud deployment."
        ),
        "strong_resume": (
            "Senior Python Developer with 6 years experience in Machine Learning, "
            "building scikit-learn models, pandas pipelines, numpy numerical routines, "
            "and deploying scalable applications on AWS EC2 and ECR."
        ),
        "moderate_resume": (
            "Software engineer with general Python backend experience, relational databases, "
            "SQL, API design, and elementary cloud knowledge."
        ),
        "unrelated_resume": (
            "Executive Chef and restaurant manager with 12 years in culinary hospitality, "
            "kitchen inventory control, fine dining, and menu curation."
        )
    }


class TestPDFExtraction:
    """Tests for PDF text extraction including edge cases and corrupted streams."""

    def test_extract_text_from_valid_pdf_sample(self):
        """Verify text extraction on actual PDF samples in repository."""
        sample_path = os.path.join(os.path.dirname(__file__), "..", "resumeSamples", "resume1.pdf")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                extracted = extract_text_from_pdf(f)
            assert isinstance(extracted, str)
            assert len(extracted.strip()) > 50
        else:
            pytest.skip(f"Sample PDF not found at {sample_path}")

    def test_extract_text_from_empty_stream(self):
        """Verify handling of completely empty file/byte buffer without crashing."""
        empty_stream = io.BytesIO(b"")
        extracted = extract_text_from_pdf(empty_stream)
        assert extracted == ""

    def test_extract_text_from_corrupted_stream(self):
        """Verify handling of corrupted or non-PDF bytes returns empty string safely."""
        corrupted_stream = io.BytesIO(b"NOT_A_VALID_PDF_HEADER_OR_CONTENT")
        extracted = extract_text_from_pdf(corrupted_stream)
        assert extracted == ""


class TestTFIDFAndCosineSimilarity:
    """Tests for NLP vectorization, similarity bounds, and ranking order."""

    def test_similarity_score_validity_and_bounds(self, sample_data):
        """Verify similarity scores are strictly numerical and bounded within [0.0, 100.0]."""
        resumes = [
            sample_data["strong_resume"],
            sample_data["moderate_resume"],
            sample_data["unrelated_resume"]
        ]
        scores = rank_resumes(sample_data["jd"], resumes)

        assert len(scores) == len(resumes)
        for s in scores:
            assert isinstance(s, (float, np.floating))
            assert 0.0 <= s <= 100.0

    def test_ranking_order_semantic_relevance(self, sample_data):
        """Verify strong candidate matches outrank moderate, and moderate outrank unrelated."""
        resumes = [
            sample_data["unrelated_resume"],
            sample_data["strong_resume"],
            sample_data["moderate_resume"]
        ]
        scores = rank_resumes(sample_data["jd"], resumes)

        unrelated_score = scores[0]
        strong_score = scores[1]
        moderate_score = scores[2]

        assert strong_score > moderate_score, f"Strong ({strong_score}) should beat Moderate ({moderate_score})"
        assert moderate_score > unrelated_score, f"Moderate ({moderate_score}) should beat Unrelated ({unrelated_score})"

    def test_identical_text_maximum_similarity(self, sample_data):
        """Verify identical text produces near 100% similarity score."""
        scores = rank_resumes(sample_data["jd"], [sample_data["jd"]])
        assert len(scores) == 1
        assert pytest.approx(scores[0], abs=0.5) == 100.0

    def test_zero_matching_vocabulary(self):
        """Verify completely disjoint vocabulary produces 0.0% similarity."""
        jd = "Quantum physics entanglement photon superconductor"
        resume = "Baking chocolate chip cookies flour sugar butter oven"
        scores = rank_resumes(jd, [resume])
        assert scores[0] == 0.0

    def test_empty_resume_list_handling(self, sample_data):
        """Verify graceful return when resume list is empty."""
        scores = rank_resumes(sample_data["jd"], [])
        assert len(scores) == 0
        assert isinstance(scores, np.ndarray)

    def test_empty_job_description_handling(self, sample_data):
        """Verify graceful return when job description is empty string or whitespace."""
        scores = rank_resumes("   ", [sample_data["strong_resume"]])
        assert len(scores) == 0


class TestUIAndExportLogic:
    """Tests for score categorization, badges, tabular formatting, and CSV export."""

    def test_score_classification_thresholds(self):
        """Verify CSS score class names mapping to thresholds (>=70 high, >=40 medium, else low)."""
        assert get_score_class(88.0) == "score-high"
        assert get_score_class(70.0) == "score-high"
        assert get_score_class(69.9) == "score-medium"
        assert get_score_class(40.0) == "score-medium"
        assert get_score_class(39.9) == "score-low"
        assert get_score_class(0.0) == "score-low"

    def test_badge_thresholds(self):
        """Verify HTML badge generation according to score tiers."""
        assert "Strong Match" in get_badge(75.0)
        assert "badge-success" in get_badge(75.0)
        assert "Moderate Match" in get_badge(52.0)
        assert "badge-warning" in get_badge(52.0)
        assert "Low Match" in get_badge(15.0)
        assert "badge-info" in get_badge(15.0)

    def test_format_results_dataframe(self):
        """Verify DataFrame formatting, descending sorting, and rank assignment."""
        files = ["resume_c.pdf", "resume_a.pdf", "resume_b.pdf"]
        scores = np.array([25.0, 92.5, 65.0])
        df = format_results_dataframe(files, scores)

        assert len(df) == 3
        assert list(df.columns) == ["Rank", "Resume", "Score", "Match Level"]
        # Verify top ranked is resume_a.pdf with score 92.5
        assert df.iloc[0]["Resume"] == "resume_a.pdf"
        assert df.iloc[0]["Score"] == 92.5
        assert df.iloc[0]["Rank"] == 1
        assert "Strong Match" in df.iloc[0]["Match Level"]

        # Verify bottom ranked is resume_c.pdf
        assert df.iloc[2]["Resume"] == "resume_c.pdf"
        assert df.iloc[2]["Rank"] == 3

    def test_generate_csv_bytes(self):
        """Verify CSV export is clean, UTF-8 encoded, and strips HTML match badges."""
        files = ["cand1.pdf", "cand2.pdf"]
        scores = np.array([85.0, 45.0])
        df = format_results_dataframe(files, scores)
        csv_bytes = generate_csv_bytes(df)

        assert isinstance(csv_bytes, bytes)
        csv_text = csv_bytes.decode("utf-8")
        lines = csv_text.strip().split("\n")
        assert lines[0] == "Rank,Resume,Score"
        assert "<span" not in csv_text
        assert "cand1.pdf" in lines[1]
