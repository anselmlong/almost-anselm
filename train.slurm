#!/bin/bash
#SBATCH --job-name=almost-anselm
#SBATCH --partition=gpu-long
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --output=logs/%x-%j.out

export HF_HOME=$HOME/.cache/huggingface
export TRANSFORMERS_CACHE=$HF_HOME
export HF_DATASETS_CACHE=$HF_HOME
export WANDB_DISABLED=true

cd $HOME/almost-anselm
source venv/bin/activate

echo "Starting training!"
accelerate launch -m axolotl.cli.train configs/axolotl_config.yaml




