#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
export VLLM_USE_FLASHINFER_SAMPLER=0
exec /home/luca/fot-exp2/env-vllm/bin/vllm serve Qwen/Qwen3.8-27B-FP8 \
  --revision 017b9c7af6b5689d5dd426a76e0bc077eb5ca20a \
  --served-model-name fot-exp2-consumer \
  --host 127.0.0.1 --port 8001 \
  --tensor-parallel-size 1 --max-model-len 16384 --max-num-seqs 1 \
  --gpu-memory-utilization 0.97 --language-model-only \
  --reasoning-parser qwen3 --seed 20260829 --generation-config vllm \
  --enforce-eager --no-enable-prefix-caching \
  --kernel-config '{"enable_flashinfer_autotune":false,"enable_jit_warmup":false,"enable_cutedsl_warmup":false}'
