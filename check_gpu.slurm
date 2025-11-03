#!/bin/bash
#SBATCH --job-name=gpucheck
#SBATCH --partition=gpu          # use gpu-long if you prefer longer than 3h
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
#SBATCH --output=logs/%x-%j.out

# --- Activate your venv (adjust path if different)
source ~/almost-anselm/venv/bin/activate

echo "=== ENV ==="
hostname
date
which python
python --version
pip --version
echo

echo "=== NVIDIA SMI ==="
nvidia-smi || echo "nvidia-smi not found"
echo

echo "=== Python CUDA sanity check ==="
python - <<'PY'
import sys, torch, platform
print("Python:", sys.version)
print("Platform:", platform.platform())
print("Torch version:", torch.__version__)
print("Torch CUDA version (built with):", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("Device 0:", torch.cuda.get_device_name(0))
    x = torch.randn(1000, 1000, device="cuda")
    print("CUDA tensor OK, sum:", x.sum().item())
else:
    print("No CUDA from PyTorch. If nvidia-smi above shows a GPU, your Torch wheel may be CPU-only or mismatched.")
PY
echo

echo "=== bitsandbytes check (optional) ==="
python - <<'PY'
try:
    import bitsandbytes as bnb
    print("bitsandbytes version:", bnb.__version__)
    print("bitsandbytes CUDA setup OK.")
except Exception as e:
    print("bitsandbytes import failed:", e)
PY

