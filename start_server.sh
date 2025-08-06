#!/bin/bash
python3 -m vllm.entrypoints.openai.api_server \
  --model /workspace/model \
  --port 8000 \
  --max-model-len 8192