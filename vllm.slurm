#!/bin/bash
#SBATCH --job-name=vllm-infer
#SBATCH --partition=gpu-long
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=logs/vllm-infer-%j.out

# Activate your environment
source venv/bin/activate  # or conda activate vllm-env

# Optional: set HF token if model is private

# Run vLLM openai-compatible server with your fine-tuned model
python3 -m vllm.entrypoints.openai.api_server \
    --model anselmlong/almost-anselm \
    --tokenizer anselmlong/almost-anselm \
    --dtype float16 \
    --max-model-len 768 \
    --port 8000 \
    --host 0.0.0.0

