#!/bin/sh
#SBATCH --job-name=gpujob
#SBATCH --gpus=1

#SBATCH --output=logs/%x-%j.out

echo "Starting Inference"
axolotl inference configs/simple_axolotl.yaml --lora-model-dir="./models/base_v2"

