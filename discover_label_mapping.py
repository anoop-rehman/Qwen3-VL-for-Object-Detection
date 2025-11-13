#!/usr/bin/env python3
"""Infer class-id ↔ label mappings by cross-referencing original annotations with YOLO files."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Discover the label mapping between human-readable annotations and YOLO label files "
            "by matching boxes via IoU."
        )
    )
    parser.add_argument("original_root", type=Path, help="Directory with original *_anno.txt files.")
    parser.add_argument("yolo_root", type=Path, help="Directory with YOLO txt files.")
    parser.add_argument(
        "--orig-suffix",
        default="_anno.txt",
        help="Suffix to strip from original filenames before matching (default: %(default)s).",
    )
    parser.add_argument(
        "--yolo-suffix",
        default=".txt",
        help="Suffix for YOLO label files (default: %(default)s).",
    )
    parser.add_argument(
        "--min-iou",
        type=float,
        default=0.7,
        help="IoU threshold for pairing boxes (default: %(default)s).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional limit on number of samples to inspect (after matching filenames).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional path to write the discovered mapping as JSON (class_id -> label).",
    )
    return parser.parse_args()


def warn(message: str) -> None:
    print(f"Warning: {message}")


@dataclass
class BoxRecord:
    label: str
    box: Tuple[float, float, float, float]


def collect_label_files(root: Path, suffix: str) -> Dict[str, Path]:
    files: Dict[str, Path] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        name = path.name
        if suffix and not name.endswith(suffix):
            continue
        base = name[: -len(suffix)] if suffix else name
        if base in files:
            warn(f"Duplicate base name '{base}' detected; keeping first occurrence at {files[base]}")
            continue
        files[base] = path
    return files


def load_original_boxes(path: Path) -> List[BoxRecord]:
    records: List[BoxRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split()
            if len(parts) < 5:
                warn(f"{path}: line {line_number} malformed (expected label + 4 coords)")
                continue
            label = parts[0]
            try:
                x1, y1, x2, y2 = map(float, parts[1:5])
            except ValueError:
                warn(f"{path}: line {line_number} has non-numeric coords")
                continue
            if x2 <= x1 or y2 <= y1:
                warn(f"{path}: line {line_number} degenerate box skipped")
                continue
            records.append(BoxRecord(label=label, box=(x1, y1, x2, y2)))
    return records


def load_yolo_boxes(path: Path) -> List[Tuple[str, Tuple[float, float, float, float]]]:
    boxes: List[Tuple[str, Tuple[float, float, float, float]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split()
            if len(parts) < 5:
                warn(f"{path}: line {line_number} malformed (expected class + 4 coords)")
                continue
            class_token = parts[0]
            try:
                class_id = str(int(float(class_token)))
            except ValueError:
                class_id = class_token
            try:
                x_center, y_center, width, height = map(float, parts[1:5])
            except ValueError:
                warn(f"{path}: line {line_number} has non-numeric coords")
                continue
            x1 = max(0.0, x_center - width / 2)
            y1 = max(0.0, y_center - height / 2)
            x2 = min(1.0, x_center + width / 2)
            y2 = min(1.0, y_center + height / 2)
            if x2 <= x1 or y2 <= y1:
                warn(f"{path}: line {line_number} degenerate box skipped")
                continue
            boxes.append((class_id, (x1, y1, x2, y2)))
    return boxes


def compute_iou(box_a: Tuple[float, float, float, float], box_b: Tuple[float, float, float, float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    if inter_area <= 0.0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    denom = area_a + area_b - inter_area
    return inter_area / denom if denom > 0 else 0.0


def match_boxes(
    originals: Sequence[BoxRecord],
    yolo_boxes: Sequence[Tuple[str, Tuple[float, float, float, float]]],
    min_iou: float,
) -> List[Tuple[int, int]]:
    candidates: List[Tuple[float, int, int]] = []
    for o_idx, orig in enumerate(originals):
        for y_idx, (_, box) in enumerate(yolo_boxes):
            iou = compute_iou(orig.box, box)
            if iou >= min_iou:
                candidates.append((iou, o_idx, y_idx))

    candidates.sort(reverse=True)
    matched_orig: set[int] = set()
    matched_yolo: set[int] = set()
    matches: List[Tuple[int, int]] = []

    for _, o_idx, y_idx in candidates:
        if o_idx in matched_orig or y_idx in matched_yolo:
            continue
        matched_orig.add(o_idx)
        matched_yolo.add(y_idx)
        matches.append((o_idx, y_idx))

    return matches


def main() -> None:
    args = parse_args()
    if not args.original_root.is_dir():
        raise FileNotFoundError(f"Original root not found: {args.original_root}")
    if not args.yolo_root.is_dir():
        raise FileNotFoundError(f"YOLO root not found: {args.yolo_root}")

    orig_files = collect_label_files(args.original_root, args.orig_suffix)
    yolo_files = collect_label_files(args.yolo_root, args.yolo_suffix)

    shared_keys = sorted(set(orig_files) & set(yolo_files))
    if args.limit:
        shared_keys = shared_keys[: args.limit]

    if not shared_keys:
        print("No overlapping annotation files found between the two roots.")
        return

    mapping_counts: Dict[str, Counter[str]] = defaultdict(Counter)
    unmatched_orig_total = 0
    unmatched_yolo_total = 0
    files_used = 0

    for base in shared_keys:
        orig_path = orig_files[base]
        yolo_path = yolo_files[base]
        orig_boxes = load_original_boxes(orig_path)
        yolo_boxes = load_yolo_boxes(yolo_path)
        if not orig_boxes or not yolo_boxes:
            continue

        matches = match_boxes(orig_boxes, yolo_boxes, args.min_iou)
        matched_orig_indices = {o_idx for o_idx, _ in matches}
        matched_yolo_indices = {y_idx for _, y_idx in matches}

        unmatched_orig_total += len(orig_boxes) - len(matched_orig_indices)
        unmatched_yolo_total += len(yolo_boxes) - len(matched_yolo_indices)

        for o_idx, y_idx in matches:
            class_id = yolo_boxes[y_idx][0]
            mapping_counts[class_id][orig_boxes[o_idx].label] += 1
        files_used += 1

    if not mapping_counts:
        print("No matches were found with the chosen IoU threshold.")
        return

    print(f"Files analyzed: {files_used}")
    print(f"Unmatched original boxes: {unmatched_orig_total}")
    print(f"Unmatched YOLO boxes   : {unmatched_yolo_total}")
    print("\nDiscovered mappings:")

    discovered: Dict[str, str] = {}
    for class_id in sorted(mapping_counts, key=lambda cid: int(cid) if cid.isdigit() else cid):
        counter = mapping_counts[class_id]
        total = sum(counter.values())
        top_label, top_count = counter.most_common(1)[0]
        confidence = top_count / total
        discovered[class_id] = top_label
        print(f"class {class_id}: {top_label} ({top_count}/{total}, {confidence:.1%})")
        if len(counter) > 1:
            secondaries = ", ".join(f"{label}:{count}" for label, count in counter.most_common()[1:])
            print(f"  other candidates: {secondaries}")

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with args.output_json.open("w", encoding="utf-8") as handle:
            json.dump(discovered, handle, indent=2, ensure_ascii=False)
        print(f"\nMapping written to {args.output_json}")


if __name__ == "__main__":
    main()
