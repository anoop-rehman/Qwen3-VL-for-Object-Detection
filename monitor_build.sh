#!/bin/bash
# Monitor vLLM build progress

echo "=== Build Process Status ==="
echo ""

# Check if build is running
if pgrep -f "uv pip install" > /dev/null; then
    echo "✓ uv pip install is running"
    UV_PID=$(pgrep -f "uv pip install" | head -1)
    echo "  PID: $UV_PID"
else
    echo "✗ uv pip install not running"
    exit 1
fi

echo ""
echo "=== Compilation Processes ==="
echo ""

# Count compilation processes
CMAKE_COUNT=$(pgrep -c cmake || echo "0")
NINJA_COUNT=$(pgrep -c ninja || echo "0")
NVCC_COUNT=$(pgrep -c nvcc || echo "0")

echo "CMake processes: $CMAKE_COUNT"
echo "Ninja processes: $NINJA_COUNT"
echo "NVCC (CUDA compiler) processes: $NVCC_COUNT"

if [ "$NVCC_COUNT" -gt 0 ]; then
    echo ""
    echo "Currently compiling:"
    ps aux | grep nvcc | grep -v grep | head -3 | awk '{print "  " $11 " " $12 " " $13 " " $14 " " $15 " " $16 " " $17}'
fi

echo ""
echo "=== CPU Usage ==="
top -bn1 | grep -E "(Cpu|%Cpu)" | head -1

echo ""
echo "=== Recent Build Activity ==="
echo "Checking for recent file modifications in build directories..."

# Find the most recent build temp directory
BUILD_DIR=$(find /home/shadeform/.cache/uv/builds-v0 -type d -name ".tmp*" -newer /tmp 2>/dev/null | head -1)

if [ -n "$BUILD_DIR" ]; then
    echo "Build directory: $BUILD_DIR"
    
    # Find recently modified .o files (object files being created)
    RECENT_OBJ=$(find "$BUILD_DIR" -name "*.o" -mmin -1 2>/dev/null | wc -l)
    echo "Object files modified in last minute: $RECENT_OBJ"
    
    # Show most recently modified file
    RECENT_FILE=$(find "$BUILD_DIR" -type f -mmin -1 2>/dev/null | head -1)
    if [ -n "$RECENT_FILE" ]; then
        echo "Most recent file: $(basename $RECENT_FILE)"
        echo "  Modified: $(stat -c %y "$RECENT_FILE" 2>/dev/null | cut -d. -f1)"
    fi
else
    echo "Could not find build directory"
fi

echo ""
echo "=== Tips ==="
echo "- If NVCC processes > 0, compilation is actively running"
echo "- First compile can take 15-30 minutes"
echo "- Watch this script in a loop: watch -n 5 ./monitor_build.sh"

