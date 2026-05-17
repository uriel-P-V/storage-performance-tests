#!/bin/bash
# run_performance.sh
# ------------------
# Runs performance and benchmark tests with a summary report.
#
# Usage:
#   ./scripts/run_performance.sh           # all performance tests
#   ./scripts/run_performance.sh benchmark # benchmark only

MODE=${1:-"all"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="reports"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo "  Storage Performance Test Runner"
echo "  Mode: $MODE"
echo "  Timestamp: $TIMESTAMP"
echo "========================================"

if [ "$MODE" == "benchmark" ]; then
    pytest tests/test_benchmark.py -v \
        --benchmark-sort=mean \
        --benchmark-columns=min,max,mean,stddev,ops \
        | tee "${REPORT_DIR}/benchmark_${TIMESTAMP}.log"
else
    pytest tests/ -v -s \
        | tee "${REPORT_DIR}/performance_${TIMESTAMP}.log"
fi

EXIT_CODE=$?

echo "========================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "  RESULT: PASSED ✓"
else
    echo "  RESULT: FAILED ✗"
fi
echo "  Log: ${REPORT_DIR}/"
echo "========================================"

exit $EXIT_CODE