#!/bin/bash
#SBATCH --job-name=almost-anselm
#SBATCH --partition=gpu-long
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --output=logs/%x-%j.out

# Clean environment to avoid mismatched CUDA libs
module purge
module load cuda/12.8

export HF_HOME=$HOME/.cache/huggingface
export TRANSFORMERS_CACHE=$HF_HOME
export HF_DATASETS_CACHE=$HF_HOME
export WANDB_DISABLED=true
export HUGGINGFACE_HUB_TOKEN=

cd $HOME/almost-anselm
source ~/axo-venv/bin/activate


echo "[CHECK] GPU availability:"
nvidia-smi
python - << 'EOF'
import torch
print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device:", torch.cuda.get_device_name(0))
EOF

echo "Starting training!"
accelerate launch -m axolotl.cli.train configs/config.yaml --report_to none




