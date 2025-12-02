#!/usr/bin/env python3
"""Create a JSONL file from a single detection for visualize_results.py"""
import json
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python create_single_result.py <image_path> <detections_json> [output.jsonl]")
    print("Example: python create_single_result.py wikipedia_screenshot.png '[{\"bbox_2d\": [945, 28, 969, 50], \"label\": \"button\"}]'")
    sys.exit(1)

image_path = Path(sys.argv[1])
detections_json = sys.argv[2]
output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("results.jsonl")

# Parse detections
try:
    detections = json.loads(detections_json)
except json.JSONDecodeError as e:
    print(f"Error parsing detections JSON: {e}", file=sys.stderr)
    sys.exit(1)

# Create JSONL record
record = {
    "image": image_path.name,  # Relative path (just filename for single image)
    "detections": detections
}

# Write to JSONL file
with output_path.open("w", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Created {output_path} with detection for {image_path.name}")
