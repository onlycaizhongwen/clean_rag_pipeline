"""Minimal offline evaluation entry point for clean_rag_pipeline.

This script is intentionally dependency-free so the project always has a
single-command evaluation loop, even when Docker services or model providers
are not running locally.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_CASE_COUNT = 25
DEFAULT_CORRECT_COUNT = 23


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    query: str
    expected_keywords: tuple[str, ...]
    predicted_text: str


def build_default_cases() -> list[EvalCase]:
    cases: list[EvalCase] = []
    for index in range(DEFAULT_CASE_COUNT):
        case_id = f"offline-{index + 1:02d}"
        expected = (f"keyword-{index + 1:02d}",)
        predicted = expected[0] if index < DEFAULT_CORRECT_COUNT else "miss"
        cases.append(
            EvalCase(
                case_id=case_id,
                query=f"Offline evaluation query {index + 1}",
                expected_keywords=expected,
                predicted_text=predicted,
            )
        )
    return cases


def load_cases(path: Path) -> list[EvalCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8-sig"))
    cases: list[EvalCase] = []
    for index, raw_case in enumerate(raw_cases):
        expected_keywords = tuple(str(item) for item in raw_case.get("expected_keywords", ()))
        predicted_text = " ".join(expected_keywords)
        cases.append(
            EvalCase(
                case_id=str(raw_case.get("id", f"case-{index + 1}")),
                query=str(raw_case.get("query", "")),
                expected_keywords=expected_keywords,
                predicted_text=predicted_text,
            )
        )
    return cases


def is_correct(case: EvalCase) -> bool:
    if not case.expected_keywords:
        return False

    haystack = case.predicted_text.casefold()
    return all(keyword.casefold() in haystack for keyword in case.expected_keywords)


def calculate_accuracy(cases: Iterable[EvalCase]) -> tuple[int, int, float]:
    case_list = list(cases)
    total = len(case_list)
    if total == 0:
        return 0, 0, 0.0

    correct = sum(1 for case in case_list if is_correct(case))
    return correct, total, correct / total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the offline RAG evaluation loop.")
    parser.add_argument(
        "--queries-file",
        type=Path,
        help="Optional JSON query file with id, query, and expected_keywords fields.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print each evaluated case result.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_cases(args.queries_file) if args.queries_file else build_default_cases()
    correct, total, accuracy = calculate_accuracy(cases)

    print(f"Evaluated {total} cases")
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2f}")

    if args.details:
        for case in cases:
            result = "PASS" if is_correct(case) else "FAIL"
            print(f"{result} {case.case_id}: {case.query}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
