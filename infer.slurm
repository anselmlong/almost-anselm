#!/bin/sh
#SBATCH --job-name=gpujob
#SBATCH --gpus=1

#SBATCH --output=logs/%x-%j.out

echo "Starting Inference"
source ~/almost-anselm/venv/bin/activate
axolotl inference configs/config.yaml --lora-model-dir="./models/base_v5"

