#!/bin/sh
set -e

python -m services.inventory.grpc_server &
GRPC_PID=$!

cleanup() {
    kill "$GRPC_PID" 2>/dev/null || true
    wait "$GRPC_PID" 2>/dev/null || true
}

trap cleanup EXIT

python -m uvicorn services.inventory.main:app --host 0.0.0.0 --port 9001
