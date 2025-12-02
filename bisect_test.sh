#!/bin/bash
# Test script for git bisect - requires manual inspection
# Returns 0 if GOOD (no bug), non-zero if BAD (bug present)
# User must visually inspect the output to determine if it's correct

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Testing vLLM commit: $(git rev-parse --short HEAD)${NC}"
echo -e "${YELLOW}========================================${NC}"

# Step 1: Reinstall vLLM from current commit
echo -e "${BLUE}Step 1: Reinstalling vLLM...${NC}"
uv pip uninstall vllm >/dev/null 2>&1 || true
uv pip install -e . >/dev/null 2>&1
echo -e "${GREEN}✓ Installation complete${NC}"

# Step 2: Wait for installation
sleep 2

# Step 3: Check if server is running
echo -e "${BLUE}Step 2: Checking vLLM server...${NC}"
if ! curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo -e "${RED}✗ ERROR: vLLM server is not running on port 8000${NC}"
    echo ""
    echo "Please start the server manually in another terminal with:"
    echo ""
    echo "  python -m vllm.entrypoints.openai.api_server \\"
    echo "    --host 0.0.0.0 \\"
    echo "    --port 8000 \\"
    echo "    --model Qwen/Qwen3-VL-30B-A3B-Instruct \\"
    echo "    --served-model-name qwen-vl \\"
    echo "    --tensor-parallel-size 1 \\"
    echo "    --pipeline-parallel-size 1 \\"
    echo "    --reasoning_parser deepseek_r1 \\"
    echo "    --no-enable-prefix-caching \\"
    echo "    --max-model-len 50000"
    echo ""
    exit 1
fi
echo -e "${GREEN}✓ Server is running${NC}"

# Step 4: Run the detection and create visualization
echo -e "${BLUE}Step 3: Running detection test...${NC}"
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection

# Create a unique output filename for this commit
COMMIT_HASH=$(git -C /home/shadeform/workspace/vllm_testing/vllm rev-parse --short HEAD 2>/dev/null || echo "unknown")
OUTPUT_FILE="bisect_output_${COMMIT_HASH}.png"

# Run detection and create visualization
python detect_and_visualize.py \
    wikipedia_screenshot.png \
    "Locate the button that is used to log in" \
    --output-dir bisect_results \
    --output-filename "$OUTPUT_FILE" \
    2>&1 | tee /tmp/bisect_output.log

# Check if visualization was created
VISUALIZATION_PATH="bisect_results/$OUTPUT_FILE"
if [ ! -f "$VISUALIZATION_PATH" ]; then
    echo -e "${RED}✗ ERROR: Failed to create visualization${NC}"
    echo "Check /tmp/bisect_output.log for details"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Visualization created: $VISUALIZATION_PATH${NC}"
echo ""

# Step 5: Show the detection results
echo -e "${BLUE}Detection results:${NC}"
if [ -f "results.jsonl" ]; then
    cat results.jsonl | python -m json.tool
fi
echo ""

# Step 6: Ask user to inspect and decide
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}MANUAL INSPECTION REQUIRED${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Please inspect the visualization at:"
echo -e "${BLUE}  $VISUALIZATION_PATH${NC}"
echo ""
echo "Compare the bounding box accuracy with the expected result."
echo "In v0.11.0, the login button should be correctly located."
echo "In v0.11.1, the bounding box may be incorrect or missing."
echo ""
echo -e "${YELLOW}Is this commit GOOD (no bug) or BAD (bug present)?${NC}"
echo ""
echo "Enter:"
echo "  [g]ood  - Bounding box is correct (like v0.11.0)"
echo "  [b]ad   - Bounding box is incorrect/missing (like v0.11.1)"
echo "  [s]kip  - Cannot determine or compilation error"
echo "  [q]uit  - Exit bisect"
echo ""
read -p "Your decision: " decision

case "$decision" in
    g|good|G|GOOD)
        echo ""
        echo -e "${GREEN}✓ Marking as GOOD${NC}"
        exit 0
        ;;
    b|bad|B|BAD)
        echo ""
        echo -e "${RED}✗ Marking as BAD${NC}"
        exit 1
        ;;
    s|skip|S|SKIP)
        echo ""
        echo -e "${YELLOW}⊘ Marking as SKIP${NC}"
        exit 125  # Git bisect skip exit code
        ;;
    q|quit|Q|QUIT)
        echo ""
        echo "Exiting bisect test..."
        exit 130  # Exit code for user interruption
        ;;
    *)
        echo ""
        echo -e "${RED}Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac
