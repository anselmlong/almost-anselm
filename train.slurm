#!/bin/bash
#SBATCH --job-name=almost-anselm
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=03:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --output=logs/%x-%j.out

export HF_HOME=$HOME/.cache/huggingface
export TRANSFORMERS_CACHE=$HF_HOME
export HF_DATASETS_CACHE=$HF_HOME
export WANDB_DISABLED=true

cd $HOME/almost-anselm
source venv/bin/activate

echo "Starting training!"
accelerate launch -m axolotl.cli.train configs/simple_axolotl.yaml

