#!/usr/bin/env python3
"""
Complete workflow: Detection → JSONL → Visualization
Usage: python detect_and_visualize.py <image_path> <prompt> [output_dir]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from query_bbox import request_completion, encode_image, build_payload, extract_detections, sanitize_detections
from visualize_results import load_results, process_dataset


def main():
    parser = argparse.ArgumentParser(
        description="Run detection and create visualization in one step"
    )
    parser.add_argument("image_path", type=Path, help="Path to the image file")
    parser.add_argument("prompt", help="Detection prompt")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output_visualizations"),
        help="Output directory for visualizations (default: output_visualizations)",
    )
    parser.add_argument(
        "--api-base",
        default="http://127.0.0.1:8000/v1",
        help="API base URL (default: http://127.0.0.1:8000/v1)",
    )
    parser.add_argument(
        "--model",
        default="qwen-vl",
        help="Model name (default: qwen-vl)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=10000,
        help="Max tokens (default: 10000)",
    )
    args = parser.parse_args()

    if not args.image_path.is_file():
        print(f"Error: Image not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)

    print("Step 1: Running detection query...")
    try:
        image_data = encode_image(args.image_path)
        payload = build_payload(
            args.prompt,
            image_data,
            args.model,
            temperature=0.0,
            max_tokens=args.max_tokens,
            top_p=0.95,
            top_k=20,
            repetition_penalty=1.0,
            presence_penalty=0.0,
            seed=1,
        )
        body = request_completion(args.api_base, payload, timeout=120.0)
        detections, raw_text, raw_body, metadata = extract_detections(body)
        detections = list(detections)
        sanitized = sanitize_detections(detections)
        detections_to_use = sanitized if sanitized else detections
    except Exception as e:
        print(f"Error during detection: {e}", file=sys.stderr)
        sys.exit(1)

    if not detections_to_use:
        print("Warning: No detections found.", file=sys.stderr)

    print(f"Found {len(detections_to_use)} detection(s)")

    print("Step 2: Creating JSONL file...")
    image_name = args.image_path.name
    results_path = Path("results.jsonl")
    record = {
        "image": image_name,
        "detections": detections_to_use,
    }
    with results_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Created {results_path}")

    print("Step 3: Visualizing results...")
    dataset_root = args.image_path.parent.resolve()
    if str(dataset_root) == ".":
        dataset_root = Path(".").resolve()
    
    output_root = args.output_dir.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    results = {image_name: detections_to_use}
    processed, skipped = process_dataset(dataset_root, results, output_root, overwrite=True)
    
    print(f"\n✓ Complete! Visualization saved to: {output_root}/{args.image_path.stem}_labeled{args.image_path.suffix}")


if __name__ == "__main__":
    main()

