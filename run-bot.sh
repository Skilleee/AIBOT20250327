#!/bin/bash
cd "$(dirname "$0")"
echo "Kör GPT-refaktorering..."
python3 chatgpt.py --group --show-graph
