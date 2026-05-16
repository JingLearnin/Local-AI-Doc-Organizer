"""Rule-based document classification for Local-AI-Doc-Organizer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ClassificationResult:
    """The public result returned by the rule-based classifier."""

    category: str
    confidence: float
    reason: str
    matched_keywords: tuple[str, ...]


def classify_document(
    *,
    file_name: str,
    content: str,
    rules: dict[str, Any],
) -> ClassificationResult:
    """Classify one document using keyword rules.

    The classifier intentionally exposes an observable and stable interface:
    callers provide a file name, extracted text content, and loaded rules; the
    function returns a category, confidence score, and human-readable reason.
    """

    categories: dict[str, Any] = rules.get("categories", {})
    settings: dict[str, Any] = rules.get("settings", {})
    default_category = settings.get("default_category", "Needs_Review")
    minimum_confidence = float(settings.get("minimum_confidence", 0.6))

    haystack = f"{file_name}\n{content}".lower()
    scored_matches: list[tuple[str, tuple[str, ...], float]] = []

    for category, category_rules in categories.items():
        keywords = category_rules.get("keywords", []) if isinstance(category_rules, dict) else []
        matched = tuple(keyword for keyword in keywords if keyword.lower() in haystack)
        if not matched:
            continue

        keyword_count = max(len(keywords), 1)
        coverage_score = len(matched) / keyword_count
        confidence = min(0.95, 0.55 + (0.4 * coverage_score))
        scored_matches.append((category, matched, round(confidence, 2)))

    if not scored_matches:
        return ClassificationResult(
            category=default_category,
            confidence=0.0,
            reason="no keyword match",
            matched_keywords=(),
        )

    scored_matches.sort(key=lambda item: (item[2], len(item[1])), reverse=True)
    best_category, matched_keywords, confidence = scored_matches[0]

    if confidence < minimum_confidence:
        return ClassificationResult(
            category=default_category,
            confidence=confidence,
            reason=f"below minimum confidence; matched keywords: {', '.join(matched_keywords)}",
            matched_keywords=matched_keywords,
        )

    return ClassificationResult(
        category=best_category,
        confidence=confidence,
        reason=f"matched keywords: {', '.join(matched_keywords)}",
        matched_keywords=matched_keywords,
    )
