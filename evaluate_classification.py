#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, Optional, Pattern, Tuple


def warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute classification metrics (empty vs. non-empty detections) from detections.jsonl. "
            "Ground-truth labels are inferred from user-provided regex patterns applied to "
            "each sample's relative path."
        )
    )
    parser.add_argument("results_path", type=Path, help="JSONL detection results file.")
    parser.add_argument(
        "--positive-regex",
        required=True,
        help="Regex that identifies samples containing at least one target object.",
    )
    parser.add_argument(
        "--negative-regex",
        help="Regex that identifies samples with zero target objects. Optional when unmatched samples should be skipped.",
    )
    parser.add_argument(
        "--unmatched-policy",
        choices=["skip", "positive", "negative"],
        default="skip",
        help=(
            "How to handle samples that match neither regex. "
            "'skip' excludes them from metrics (default)."
        ),
    )
    return parser.parse_args()


def load_results(results_path: Path) -> Dict[str, bool]:
    detections: Dict[str, bool] = {}
    with results_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
                rel_path = record["image"]
                dets = record.get("detections", [])
                detections[rel_path] = bool(dets)
            except (JSONDecodeError, KeyError) as exc:
                warn(f"Skipping malformed record on line {line_number}: {exc}")
    return detections


def assign_label(
    rel_path: str,
    positive_regex: Pattern[str],
    negative_regex: Optional[Pattern[str]],
    unmatched_policy: str,
) -> Tuple[bool | None, str]:
    pos = bool(positive_regex.search(rel_path))
    neg = bool(negative_regex.search(rel_path)) if negative_regex else False

    if pos and neg:
        warn(f"Sample '{rel_path}' matches both positive and negative regexes; skipping.")
        return None, "conflict"

    if pos:
        return True, "positive"
    if neg:
        return False, "negative"

    if unmatched_policy == "positive":
        return True, "fallback_pos"
    if unmatched_policy == "negative":
        return False, "fallback_neg"
    return None, "unmatched"


def compute_metrics(tp: int, fp: int, tn: int, fn: int) -> Dict[str, float]:
    total = tp + fp + tn + fn
    def safe(dividend: float, divisor: float) -> float:
        return dividend / divisor if divisor else 0.0

    return {
        "accuracy": safe(tp + tn, total),
        "precision": safe(tp, tp + fp),
        "recall": safe(tp, tp + fn),
        "specificity": safe(tn, tn + fp),
        "f1": safe(2 * tp, 2 * tp + fp + fn),
    }


def main() -> None:
    args = parse_args()
    if not args.results_path.is_file():
        raise FileNotFoundError(f"Results file not found: {args.results_path}")

    detections = load_results(args.results_path)
    if not detections:
        print("No detections loaded from the results file.")
        return

    positive_regex = re.compile(args.positive_regex)
    negative_regex = re.compile(args.negative_regex) if args.negative_regex else None

    counts = Counter()
    skipped = Counter()

    for rel_path, predicted_positive in detections.items():
        label, reason = assign_label(
            rel_path,
            positive_regex,
            negative_regex,
            args.unmatched_policy,
        )
        if label is None:
            skipped[reason] += 1
            continue

        if label and predicted_positive:
            counts["tp"] += 1
        elif label and not predicted_positive:
            counts["fn"] += 1
        elif not label and predicted_positive:
            counts["fp"] += 1
        else:
            counts["tn"] += 1

    total_used = counts["tp"] + counts["tn"] + counts["fp"] + counts["fn"]
    print(f"Samples evaluated: {total_used}")
    if skipped:
        for reason, value in skipped.items():
            print(f"Skipped ({reason}): {value}")

    if not total_used:
        print("No samples met the criteria for evaluation.")
        return

    print("\nConfusion Matrix (predicted vs. actual):")
    print("              Actual Positive  Actual Negative")
    print(
        f"Pred Positive       {counts['tp']:>6}              {counts['fp']:>6}"
    )
    print(
        f"Pred Negative       {counts['fn']:>6}              {counts['tn']:>6}"
    )

    metrics = compute_metrics(counts["tp"], counts["fp"], counts["tn"], counts["fn"])
    print("\nMetrics:")
    for name, value in metrics.items():
        print(f"{name.title():<12}: {value:.4f}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
