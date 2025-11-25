#!/bin/bash
#SBATCH --job-name=merge-lora
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --output=logs/%x-%j.out

# Activate your environment
cd $HOME/almost-anselm
source venv/bin/activate

# Run merge script
python3 src/inference/merge.py

