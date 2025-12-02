#!/bin/bash
# Simplified test script for git bisect
# Assumes vLLM server is already running on port 8000
# Returns 0 if GOOD (no bug), non-zero if BAD (bug present)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing vLLM commit: $(git rev-parse --short HEAD)${NC}"

# Step 1: Reinstall vLLM from current commit
echo "Uninstalling existing vLLM..."
uv pip uninstall vllm >/dev/null 2>&1 || true

echo "Installing vLLM from source (editable mode)..."
uv pip install -e . >/dev/null 2>&1

# Step 2: Wait for installation
sleep 2

# Step 3: Check if server is running (you'll need to restart it manually after install)
echo "Checking if server is running..."
if ! curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo -e "${RED}ERROR: vLLM server is not running on port 8000${NC}"
    echo "Please start the server manually with:"
    echo "  python -m vllm.entrypoints.openai.api_server --host 0.0.0.0 --port 8000 --model Qwen/Qwen3-VL-30B-A3B-Instruct --served-model-name qwen-vl --tensor-parallel-size 1 --pipeline-parallel-size 1 --reasoning_parser deepseek_r1 --no-enable-prefix-caching --max-model-len 50000"
    exit 1
fi

# Step 4: Run the test
echo "Running detection test..."
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection

# Run the query and capture output
OUTPUT=$(python query_bbox.py wikipedia_screenshot.png "Locate the button that is used to log in" 2>&1)

# Check if we got valid detections
if echo "$OUTPUT" | grep -q '"bbox_2d"'; then
    # Extract the bbox coordinates
    BBOX=$(echo "$OUTPUT" | grep -o '"bbox_2d": \[[0-9, ]*\]' | head -1)
    
    if [ -n "$BBOX" ]; then
        # Extract coordinates
        COORDS=$(echo "$BBOX" | grep -o '[0-9]*' | tr '\n' ' ')
        X1=$(echo $COORDS | awk '{print $1}')
        Y1=$(echo $COORDS | awk '{print $2}')
        X2=$(echo $COORDS | awk '{print $3}')
        Y2=$(echo $COORDS | awk '{print $4}')
        
        # Check if coordinates are valid and reasonable
        # For Wikipedia login button, expected: [945, 28, 969, 50]
        # We'll accept anything reasonable (not empty, valid range)
        if [ -n "$X1" ] && [ "$X1" -gt 0 ] && [ "$X1" -lt 2000 ] && \
           [ -n "$Y1" ] && [ "$Y1" -gt 0 ] && [ "$Y1" -lt 2000 ] && \
           [ -n "$X2" ] && [ "$X2" -gt "$X1" ] && \
           [ -n "$Y2" ] && [ "$Y2" -gt "$Y1" ]; then
            echo -e "${GREEN}✓ GOOD: Got valid bounding box: $BBOX${NC}"
            exit 0
        else
            echo -e "${RED}✗ BAD: Got invalid bounding box coordinates: $BBOX${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ BAD: No bounding box found in output${NC}"
        echo "Output: $OUTPUT"
        exit 1
    fi
else
    echo -e "${RED}✗ BAD: No detections found or error occurred${NC}"
    echo "Output: $OUTPUT"
    exit 1
fi

