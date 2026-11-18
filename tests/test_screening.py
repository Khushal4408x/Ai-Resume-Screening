"""
tests/test_screening.py - Automated test suite for AI Resume Screening System.
Covers PDF text extraction, TF-IDF vectorization, similarity scoring, and ranking order.
"""

import unittest
import os
import io
import numpy as np
import pandas as pd
from resume_utils import (
    extract_text_from_pdf,
    rank_resumes,
    get_score_class,
    get_badge
)


class TestResumeScreening(unittest.TestCase):
    """Test suite covering resume text extraction, NLP vectorization, and ranking logic."""

    def setUp(self):
        self.sample_jd = (
            "Senior Python Developer with strong background in Machine Learning, "
            "scikit-learn, pandas, and cloud deployments on AWS."
        )
        self.strong_resume = (
            "Experienced Senior Python Developer with 5 years building Machine Learning "
            "pipelines using scikit-learn, pandas, numpy, and deploying applications on AWS cloud."
        )
        self.moderate_resume = (
            "Software engineer skilled in Python programming, SQL databases, and general "
            "backend web development with some cloud basics."
        )
        self.unrelated_resume = (
            "Professional Head Chef and culinary specialist with 10 years experience "
            "in Mediterranean restaurant management and menu design."
        )

    def test_extract_text_from_pdf_sample(self):
        """Verify text extraction works correctly on actual PDF samples in repository."""
        sample_path = os.path.join(os.path.dirname(__file__), "..", "resumeSamples", "resume1.pdf")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                extracted_text = extract_text_from_pdf(f)
            self.assertIsInstance(extracted_text, str)
            self.assertGreater(len(extracted_text.strip()), 50, "Extracted text should not be empty")
        else:
            self.skipTest(f"Sample PDF not found at {sample_path}")

    def test_similarity_score_generation(self):
        """Verify TF-IDF cosine similarity scores are generated within the 0 to 100 range."""
        resumes = [self.strong_resume, self.moderate_resume, self.unrelated_resume]
        scores = rank_resumes(self.sample_jd, resumes)

        self.assertEqual(len(scores), len(resumes))
        for score in scores:
            self.assertGreaterEqual(score, 0.0, "Score cannot be negative")
            self.assertLessEqual(score, 100.0, "Score cannot exceed 100.0")

    def test_ranking_order(self):
        """Verify that relevant resumes receive higher similarity scores than irrelevant ones."""
        resumes = [self.unrelated_resume, self.strong_resume, self.moderate_resume]
        scores = rank_resumes(self.sample_jd, resumes)

        unrelated_score = scores[0]
        strong_score = scores[1]
        moderate_score = scores[2]

        self.assertGreater(
            strong_score, moderate_score,
            f"Strong match ({strong_score}) must score higher than moderate match ({moderate_score})"
        )
        self.assertGreater(
            moderate_score, unrelated_score,
            f"Moderate match ({moderate_score}) must score higher than unrelated ({unrelated_score})"
        )

        # Verify DataFrame ranking matches application display logic
        df = pd.DataFrame({
            "Resume": ["Unrelated", "Strong", "Moderate"],
            "Score": scores
        }).sort_values(by="Score", ascending=False).reset_index(drop=True)
        df["Rank"] = range(1, len(df) + 1)

        self.assertEqual(df.iloc[0]["Resume"], "Strong", "Top ranked resume must be Strong")
        self.assertEqual(df.iloc[0]["Rank"], 1)

    def test_identical_text_high_similarity(self):
        """Verify identical text produces near 100% similarity score."""
        scores = rank_resumes(self.sample_jd, [self.sample_jd])
        self.assertAlmostEqual(scores[0], 100.0, delta=0.5)

    def test_empty_resumes_list(self):
        """Verify function gracefully handles empty resume list."""
        scores = rank_resumes(self.sample_jd, [])
        self.assertEqual(len(scores), 0)

    def test_score_class_thresholds(self):
        """Verify CSS score classification logic."""
        self.assertEqual(get_score_class(85.0), "score-high")
        self.assertEqual(get_score_class(70.0), "score-high")
        self.assertEqual(get_score_class(69.9), "score-medium")
        self.assertEqual(get_score_class(40.0), "score-medium")
        self.assertEqual(get_score_class(39.9), "score-low")
        self.assertEqual(get_score_class(0.0), "score-low")

    def test_badge_thresholds(self):
        """Verify HTML badge generation logic."""
        self.assertIn("Strong Match", get_badge(75.0))
        self.assertIn("badge-success", get_badge(75.0))
        self.assertIn("Moderate Match", get_badge(50.0))
        self.assertIn("badge-warning", get_badge(50.0))
        self.assertIn("Low Match", get_badge(20.0))
        self.assertIn("badge-info", get_badge(20.0))


if __name__ == "__main__":
    unittest.main()
