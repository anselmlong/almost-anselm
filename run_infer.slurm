#!/bin/bash
#SBATCH --job-name=infer
#SBATCH --partition=long                      # or gpu, if needed
#SBATCH --gres=gpu:1                          # remove if CPU-only
#SBATCH --mem=32G                             # adjust as needed
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --output=logs/infer_%j.log

source ~/almost-anselm/venv/bin/activate
python src/inference/infer.py

