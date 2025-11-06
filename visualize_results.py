#!/usr/bin/env python3
import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image

from query_bbox import render_bounding_boxes, sanitize_detections


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize detection results by creating side-by-side originals and annotated images."
    )
    parser.add_argument("dataset_root", type=Path, help="Root directory of the dataset.")
    parser.add_argument("results_path", type=Path, help="JSONL detection results file.")
    parser.add_argument("output_root", type=Path, help="Destination directory for visualizations.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing labeled images (default: skip existing).",
    )
    return parser.parse_args()


def load_results(results_path: Path) -> Dict[str, List[Dict[str, Any]]]:
    detections: Dict[str, List[Dict[str, Any]]] = {}
    with results_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
                image_key = record["image"]
                dets = record.get("detections", [])
                sanitized = sanitize_detections(dets)
                detections[image_key] = sanitized if sanitized else dets
            except (JSONDecodeError, KeyError) as exc:
                print(f"Warning: skipping malformed record at line {line_number}: {exc}")
    return detections


def build_output_path(
    dataset_root: Path,
    output_root: Path,
    rel_path: Path,
) -> Path:
    rel_parent = rel_path.parent
    base_name = rel_path.stem + "_labeled"
    extension = rel_path.suffix or ".png"
    if rel_parent == Path("."):
        target_dir = output_root
    else:
        target_dir = output_root / rel_parent
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{base_name}{extension}"


def create_side_by_side(
    original: Image.Image,
    annotated: Image.Image,
) -> Image.Image:
    width, height = original.size
    annotated = annotated.resize((width, height))
    combined = Image.new("RGB", (width * 2, height))
    combined.paste(original, (0, 0))
    combined.paste(annotated, (width, 0))
    return combined


def process_dataset(
    dataset_root: Path,
    results: Dict[str, List[Dict[str, Any]]],
    output_root: Path,
    overwrite: bool,
) -> Tuple[int, int]:
    processed = 0
    skipped = 0
    for rel_path_str, detections in results.items():
        rel_path = Path(rel_path_str)
        source_image = dataset_root / rel_path
        if not source_image.is_file():
            print(f"Warning: skipping missing image {rel_path}")
            skipped += 1
            continue

        output_path = build_output_path(dataset_root, output_root, rel_path)
        if output_path.exists() and not overwrite:
            skipped += 1
            continue

        original = Image.open(source_image).convert("RGB")
        annotated = render_bounding_boxes(original, detections)
        combined = create_side_by_side(original, annotated)
        combined.save(output_path)
        processed += 1
        print(f"Labeled image written to {output_path}")
    return processed, skipped


def main() -> None:
    args = parse_args()
    dataset_root = args.dataset_root.resolve()
    results_path = args.results_path.resolve()
    output_root = args.output_root.resolve()

    if not dataset_root.is_dir():
        raise FileNotFoundError(f"Dataset root not found or not a directory: {dataset_root}")
    if not results_path.is_file():
        raise FileNotFoundError(f"Results file not found: {results_path}")
    output_root.mkdir(parents=True, exist_ok=True)

    results = load_results(results_path)
    if not results:
        print("No detections found in the results file.")
        return

    processed, skipped = process_dataset(dataset_root, results, output_root, args.overwrite)
    print(f"Visualization complete. Processed: {processed}, skipped: {skipped}")


if __name__ == "__main__":
    main()
