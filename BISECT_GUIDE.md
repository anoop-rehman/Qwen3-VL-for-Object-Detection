# Step-by-Step Git Bisect Guide for vLLM Grounding Bug

This guide will walk you through finding the exact commit that introduced the grounding accuracy regression.

## Prerequisites

- You've already reproduced the bug (v0.11.1 broken, v0.11.0 works)
- You have a vLLM server setup that works
- You have the test image (`wikipedia_screenshot.png`) ready

---

## Step 1: Clone the vLLM Repository

```bash
cd /home/shadeform/workspace/vllm_testing
git clone https://github.com/vllm-project/vllm.git
cd vllm
```

Verify it worked:
```bash
git log --oneline -5  # Should show recent commits
```

---

## Step 2: Set Up Your Virtual Environment

**Recommendation: Use Option B (new environment)** - This keeps your bisect work isolated and prevents conflicts with your existing setup.

You can either:
- **Option A**: Use your existing virtual environment (not recommended for bisect)
- **Option B**: Create a new one specifically for bisecting ✅ **RECOMMENDED**

### Option A: Use Existing Environment

⚠️ **Not recommended** - Risk of dependency conflicts when switching between commits.

```bash
# Activate your existing venv
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
source .venv/bin/activate  # or wherever your venv is
```

### Option B: Create New Environment ✅ **RECOMMENDED**

**Why this is better:**
- ✅ Clean, isolated environment
- ✅ No risk of breaking your existing setup
- ✅ Easy to delete when done
- ✅ Avoids dependency conflicts between commits
- ✅ Can keep your main environment untouched

```bash
cd /home/shadeform/workspace/vllm_testing/vllm
uv venv .venv
source .venv/bin/activate

# Check your system's CUDA version
echo "Checking system CUDA version..."
ls -d /usr/local/cuda* 2>/dev/null || echo "CUDA not found in /usr/local"

# Install PyTorch with CUDA
# vLLM 0.11.0/0.11.1 support CUDA 12.x
# Your system has CUDA 12.8, so use cu128:
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Alternative CUDA versions (if cu128 doesn't work):
#   CUDA 12.4: --index-url https://download.pytorch.org/whl/cu124
#   CUDA 12.1: --index-url https://download.pytorch.org/whl/cu121
#   CUDA 11.8: --index-url https://download.pytorch.org/whl/cu118

# Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
```

---

## Step 3: Verify Tagged Versions Exist

Check that the version tags are available:

```bash
git tag | grep "v0.11"
```

You should see `v0.11.0` and `v0.11.1` (or similar).

**Note on CUDA Version**: Your system has **CUDA 12.8** installed. vLLM 0.11.0/0.11.1 support CUDA 12.x, so using `cu128` (CUDA 12.8) is appropriate. If you encounter issues, you can try `cu124` or `cu121` as alternatives.

---

## Step 4: Initial Setup - Install vLLM from Source

Before starting bisect, let's make sure editable install works. **Note:** `uv pip install -e .` installs from whatever git commit/tag is currently checked out. For initial setup, you can use any version (we'll switch versions during bisect).

```bash
# Make sure you're in the vllm repo directory
cd /home/shadeform/workspace/vllm_testing/vllm

# Check what commit/tag is currently checked out (optional)
git describe --tags --exact-match 2>/dev/null || git rev-parse --short HEAD

# Uninstall any existing vLLM
uv pip uninstall vllm

# Install from source in editable mode
# This installs whatever commit is currently checked out
uv pip install -e .
```

This may take a few minutes. Verify it worked:

```bash
python -c "import vllm; print(vllm.__file__)"
# Should point to your cloned repo, not site-packages
```

---

## Step 5: Verify Test Script is Ready

Make sure the bisect test script is executable:

```bash
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
chmod +x bisect_test.sh
ls -la bisect_test.sh  # Should show it's executable
```

---

## Step 6: Pre-Bisect Verification

Before starting bisect, verify your test works on known good/bad versions:

### Test v0.11.0 (should be GOOD):

```bash
cd /home/shadeform/workspace/vllm_testing/vllm
git checkout v0.11.0
uv pip uninstall vllm
uv pip install -e .

# Start server in another terminal (keep it running)
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

# In original terminal, run test
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
./bisect_test.sh
# When prompted, mark it as "good" (g)
```

### Test v0.11.1 (should be BAD):

```bash
# Stop the server (Ctrl+C in the server terminal)

cd /home/shadeform/workspace/vllm_testing/vllm
git checkout v0.11.1
uv pip uninstall vllm
uv pip install -e .

# Start server again
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

# Run test
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
./bisect_test.sh
# When prompted, mark it as "bad" (b)
```

If both tests work as expected, you're ready for bisect!

---

## Step 7: Start Git Bisect

Now the actual bisect process:

```bash
cd /home/shadeform/workspace/vllm_testing/vllm

# Start bisect
git bisect start

# Mark the known bad commit (v0.11.1)
git bisect bad v0.11.1

# Mark the known good commit (v0.11.0)
git bisect good v0.11.0
```

Git will now checkout a commit roughly halfway between v0.11.0 and v0.11.1.

---

## Step 8: The Bisect Loop

For each commit git checks out, follow these steps:

### 8.1: Reinstall vLLM

```bash
# Make sure you're in the vllm repo directory
cd /home/shadeform/workspace/vllm_testing/vllm

# Uninstall and reinstall
uv pip uninstall vllm
uv pip install -e .
```

**Note**: This may take 1-5 minutes depending on whether C++/CUDA code changed.

### 8.2: Restart the Server

**Important**: You need to restart the server after each install to use the new code.

In a **separate terminal** (keep it open):

```bash
# Stop any existing server
pkill -f "vllm.*api_server"

# Start new server
cd /home/shadeform/workspace/vllm_testing/vllm
source .venv/bin/activate  # if using new venv, or your existing one

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
```

Wait for the server to be ready (check the logs or wait ~30 seconds).

### 8.3: Run the Test

In your **original terminal**:

```bash
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
./bisect_test.sh
```

The script will:
1. Reinstall vLLM (you already did this, but it's safe to do again)
2. Check if server is running
3. Run the detection test
4. Create a visualization image
5. Show you the detection results
6. **Ask you to inspect and decide**

### 8.4: Inspect and Decide

The script will show you:
- The path to the visualization image
- The detection JSON results

**Open the visualization image** and compare it to what you know:
- **v0.11.0**: Login button should be correctly located (around [945, 28, 969, 50])
- **v0.11.1**: Bounding box may be wrong or missing

When prompted, enter:
- `g` or `good` - Bounding box is correct (like v0.11.0)
- `b` or `bad` - Bounding box is incorrect (like v0.11.1)
- `s` or `skip` - Can't determine or there's a compilation error
- `q` or `quit` - Exit bisect

### 8.5: Tell Git Your Decision

After you enter your decision in the script, it will automatically return the right exit code. But if you need to manually tell git:

```bash
# If the test showed it's GOOD:
git bisect good

# If the test showed it's BAD:
git bisect bad

# If you can't determine (compilation error, etc.):
git bisect skip
```

### 8.6: Repeat

Git will automatically checkout the next commit. Go back to **Step 8.1** and repeat.

You'll typically need to do this **11-12 times** (log₂ of ~1500 commits).

---

## Step 9: Finding the Bad Commit

After several iterations, git will tell you:

```
<commit-hash> is the first bad commit
commit <commit-hash>
Author: ...
Date: ...
    <commit message>
```

**Congratulations!** You found the commit that introduced the bug.

---

## Step 10: Investigate the Bad Commit

```bash
# Reset bisect state (get back to normal)
git bisect reset

# Check out the bad commit
git checkout <bad-commit-hash>

# View what changed in this commit
git show <bad-commit-hash>

# Or see the diff vs its parent
git diff <bad-commit-hash>^ <bad-commit-hash>
```

Look for changes related to:
- CUDA graphs
- Compilation logic
- Scheduler/batching code
- Code that's conditional on eager vs CUDA graph mode
- Any changes to the model execution path

---

## Step 11: Save Your Findings

Save the commit hash and your findings:

```bash
# Save the commit info
git show <bad-commit-hash> > /home/shadeform/workspace/vllm_testing/bad_commit_info.txt

# Save the diff
git diff <bad-commit-hash>^ <bad-commit-hash> > /home/shadeform/workspace/vllm_testing/bad_commit_diff.txt
```

---

## Tips & Troubleshooting

### Server Management

- **Keep the server terminal open** - Don't close it between bisect steps
- **Restart after each install** - The server needs to reload the new code
- **Check server logs** - If something fails, check the server terminal output

### Speeding Things Up

- **Skip compilation-heavy commits**: If a commit fails to compile or takes too long, use `git bisect skip`
- **Save bisect state**: If you need to stop and resume later:
  ```bash
  git bisect log > bisect_log.txt
  # Later...
  git bisect replay bisect_log.txt
  ```

### Common Issues

1. **"Server not running" error**: Make sure you started the server in another terminal
2. **Compilation errors**: Use `git bisect skip` and git will try another commit
3. **Wrong decision**: You can't undo, but you can restart bisect if needed
4. **Script fails**: Check `/tmp/bisect_output.log` for error details

### Visualization Files

All visualization images are saved in:
```
/home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection/bisect_results/
```

Each file is named: `bisect_output_<commit-hash>.png`

You can compare them side-by-side to see the progression of the bug.

---

## Quick Reference Commands

```bash
# Start bisect
git bisect start
git bisect bad v0.11.1
git bisect good v0.11.0

# For each commit:
cd /home/shadeform/workspace/vllm_testing/vllm
uv pip uninstall vllm && uv pip install -e .
# (Restart server in another terminal)
cd /home/shadeform/workspace/vllm_testing/Qwen3-VL-for-Object-Detection
./bisect_test.sh

# When done:
git bisect reset
```

---

## Expected Timeline

- **Each iteration**: 5-10 minutes (install + test + inspection)
- **Total iterations**: ~11-12
- **Total time**: ~2-3 hours (depending on compilation time)

Good luck! 🚀

