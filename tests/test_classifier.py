import unittest

from organizer.classifier import classify_document


RULES = {
    "categories": {
        "Career": {"keywords": ["resume", "interview", "linkedin"]},
        "Engineering": {"keywords": ["api", "database", "cloud", "python"]},
        "Finance": {"keywords": ["tuition", "receipt", "bank"]},
    },
    "settings": {"default_category": "Needs_Review", "minimum_confidence": 0.6},
}


class ClassifierTests(unittest.TestCase):
    def test_classifies_engineering_document_from_content_keywords(self):
        result = classify_document(
            file_name="notes.md",
            content="This document explains cloud architecture, API boundaries, and database indexing.",
            rules=RULES,
        )

        self.assertEqual(result.category, "Engineering")
        self.assertGreaterEqual(result.confidence, 0.6)
        self.assertIn("cloud", result.matched_keywords)
        self.assertIn("matched keywords", result.reason)

    def test_classifies_career_document_from_file_name(self):
        result = classify_document(
            file_name="resume_notes.md",
            content="Draft bullets for applications.",
            rules=RULES,
        )

        self.assertEqual(result.category, "Career")
        self.assertGreaterEqual(result.confidence, 0.6)
        self.assertIn("resume", result.matched_keywords)

    def test_sends_unknown_document_to_needs_review(self):
        result = classify_document(
            file_name="random_scan.txt",
            content="A short note with no configured category terms.",
            rules=RULES,
        )

        self.assertEqual(result.category, "Needs_Review")
        self.assertEqual(result.confidence, 0.0)
        self.assertEqual(result.reason, "no keyword match")


if __name__ == "__main__":
    unittest.main()
