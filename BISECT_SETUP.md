# Git Bisect Setup for vLLM Grounding Bug

This guide will help you find the exact commit that introduced the grounding accuracy regression between vLLM 0.11.0 and 0.11.1.

## Step 1: Clone vLLM Repository

```bash
cd /home/shadeform/workspace/vllm_testing
git clone https://github.com/vllm-project/vllm.git
cd vllm
```

## Step 2: Set Up Virtual Environment

```bash
# Create/activate your virtual environment (if not already done)
# If using uv:
uv venv .venv
source .venv/bin/activate

# Or if using standard venv:
python -m venv .venv
source .venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Install build dependencies and PyTorch (adjust for your CUDA version)
# You'll need the same setup you used for 0.11.0/0.11.1
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other vLLM dependencies
uv pip install -e ".[all]"
```

## Step 4: Verify Setup

```bash
# Check that Python sees the local checkout
python -c "import vllm; print(vllm.__file__)"
# Should point to your cloned repo, not site-packages

# Check current commit
git rev-parse HEAD
```

## Step 5: Prepare Test Script

The test script `bisect_test_simple.sh` is already created. It:
- Reinstalls vLLM from the current commit
- Tests the grounding accuracy with your Wikipedia screenshot
- Returns 0 (good) if bounding boxes are valid, non-zero (bad) if broken

**Important:** This script assumes the vLLM server is already running. You'll need to restart it manually after each `pip install -e .` during bisect.

## Step 6: Manual Bisect Workflow

### Option A: Manual (Recommended for first time)

```bash
# 1. Start bisect
git bisect start

# 2. Mark known bad commit (0.11.1)
git bisect bad v0.11.1

# 3. Mark known good commit (0.11.0)
git bisect good v0.11.0

# Git will now checkout a commit halfway between
```

Now for each commit git checks out:

```bash
# 1. Reinstall vLLM
uv pip uninstall vllm
uv pip install -e .

# 2. Restart vLLM server (in another terminal)
# Stop the old one first:
pkill -f "vllm.*api_server"

# Start new one:
python -m vllm.entrypoints.openai.api_server \
    --host 0.0.0.0 \
    --port 8000 \
    --model Qwen/Qwen3-VL-30B-A3B-Instruct \
    --served-model-name qwen-vl \
    --tensor-parallel-size 1 \
    --pipeline-parallel-size 1 \
    --reasoning_parser deepseek_r1 \
    --no-enable-prefix-caching \
    --max-model-len 50000

# 3. Wait for server to be ready (check /health endpoint)

# 4. Run test
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
./bisect_test_simple.sh

# 5. Based on result:
#    - If test passes (exit code 0): git bisect good
#    - If test fails (exit code non-zero): git bisect bad

# Repeat until git finds the first bad commit
```

### Option B: Automatic (Advanced)

If you want to automate the server restart, you can modify `bisect_test_simple.sh` to handle it, but it's more complex and slower.

## Step 7: After Finding the Bad Commit

```bash
# Reset bisect state
git bisect reset

# Check out the bad commit
git checkout <bad-commit-hash>

# View the changes
git show <bad-commit-hash>
# or
git diff <bad-commit-hash>^ <bad-commit-hash>

# Look for changes related to:
# - CUDA graphs
# - Compilation logic
# - Scheduler/batching
# - Code conditional on eager vs CUDA graph mode
```

## Tips

1. **Keep server running**: The test script assumes the server is running. Restart it after each install.

2. **Fast test**: Make sure your test is quick. The current test uses a single image which should be fast.

3. **Save intermediate results**: You might want to save the commit hash and test result at each step in case you need to resume.

4. **Skip problematic commits**: If a commit doesn't compile or has other issues, you can skip it:
   ```bash
   git bisect skip
   ```

5. **Resume bisect**: If you need to stop and resume:
   ```bash
   git bisect log > bisect_log.txt  # Save state
   # Later...
   git bisect replay bisect_log.txt  # Resume
   ```

## Expected Outcome

After ~11-12 iterations, git will tell you:
```
<commit-hash> is the first bad commit
```

Then you can investigate that commit's changes to find the root cause!

