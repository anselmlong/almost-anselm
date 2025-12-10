#!/bin/bash
#SBATCH --job-name=vllm-infer
#SBATCH --partition=gpu-long
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --output=logs/vllm-infer-%j.out

# Activate your environment
source ~/axo-venv/bin/activate  # or conda activate vllm-env

# Optional: set HF token if model is private

# Run vLLM openai-compatible server with your fine-tuned model
vllm serve anselmlong/almost-anselm \
  --dtype auto \
  --port 8000


