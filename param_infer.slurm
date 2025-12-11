#!/bin/bash
#SBATCH --job-name=param-infer
#SBATCH --partition=long
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --output=logs/param_infer_%j.log

# Parameterized inference script
# Usage: sbatch param_infer.slurm "Your prompt here"
# Or:    sbatch param_infer.slurm prompts_file.txt

source ~/almost-anselm/venv/bin/activate
cd ~/almost-anselm

PROMPT_INPUT="$1"

if [ -z "$PROMPT_INPUT" ]; then
    echo "❌ Error: No prompt provided!"
    echo "Usage: sbatch param_infer.slurm \"Your prompt here\""
    echo "   or: sbatch param_infer.slurm prompts_file.txt"
    exit 1
fi

echo "🚀 Starting Anselm AI inference..."

# Check if input is a file or direct prompt
if [ -f "$PROMPT_INPUT" ]; then
    echo "📄 Processing prompts from file: $PROMPT_INPUT"
    
    # Process each line in the file
    while IFS= read -r prompt || [ -n "$prompt" ]; do
        if [[ -n "$prompt" && ! "$prompt" =~ ^[[:space:]]*# ]]; then
            echo ""
            echo "🧑 PROMPT: $prompt"
            echo "🤖 RESPONSE:"
            echo "$prompt" | axolotl inference configs/config.yaml --lora-model-dir="./models/base_v5"
            echo "-" | tr '-' '-' | head -c 50
            echo ""
        fi
    done < "$PROMPT_INPUT"
else
    echo "💬 Processing single prompt: $PROMPT_INPUT"
    echo "🤖 RESPONSE:"
    echo "$PROMPT_INPUT" | axolotl inference configs/config.yaml --lora-model-dir="./models/base_v5"
fi

echo ""
echo "✅ Inference completed!"