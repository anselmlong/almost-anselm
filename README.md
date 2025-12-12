# 🤖 Almost Anselm: Cloning my Telegram Personality by Fine Tuning an LLM

A Telegram bot fine-tuned on my real conversation style, capable of chatting like me. Built with open-source tools: Axolotl, QLoRA, Mistral-7B, Telethon.
Check out the full blog post here: [Almost Anselm](https://anselmlong.com/blog/almost-anselm)

**Note: This README is generated with AI tools.**

---

## 🚀 Overview

Pipeline:
1. ✅ Pull Telegram messages (your side of conversations)
2. ✅ Clean + anonymize data
3. ✅ Build supervised training dataset (context → your reply)
4. ✅ Fine-tune a 7B model with QLoRA
5. ✅ Run Inference with Axolotl
---

## 🧱 Tech Stack

| Component | Tool |
|---------|------|
| LLM Base | Mistral-7B-Instruct / Llama-3-8B-Instruct |
| Fine-tuning | Axolotl + QLoRA |
| Telegram Integration | Telethon |
| Inference | Axolotl |

---

## 📦 Setup & Installation

### 1️⃣ Clone Repo
    git clone https://github.com/anselmlong/almost-anselm.git
    cd almost-anselm

### 2️⃣ Create Environment
    # Using conda (recommended)
    conda create -n anselm-ai python=3.10
    conda activate anselm-ai
    
    # OR using venv
    python -m venv venv
    source venv/bin/activate  # Mac/Linux

### 3️⃣ Install Requirements
    pip install -r requirements.txt

### 4️⃣ Create Environment Variables
Copy `.env.example` → `.env` and fill in:

    TG_API_ID=
    TG_API_HASH=
    BOT_TOKEN=
    HF_TOKEN=    # optional, if pulling private HF models

---

## 📥 Data Collection

Pull your Telegram messages:

    cd src/data
    python pull_telegram.py

➡ Output → `data/raw/messages.json`

---

## 🛁 Clean & Process Data

    # Clean and anonymize messages
    python src/data/build_dataset.py
    

➡ Outputs: 
- `data/processed/cleaned_messages.jsonl`
- `data/processed/sft_train_new.jsonl`
- `data/processed/sft_val_new.jsonl`

---

## Inference

### Method 1: SLURM Inference Scripts
    
    # Parameterized (flexible)
    sbatch param_infer.slurm "Your prompt here"
    sbatch param_infer.slurm prompts_file.txt


### Method 2: Original Axolotl Method
    # Edit prompt.txt, then:
    sbatch run_infer.slurm



## 🧠 QLoRA Fine-Tuning

Configuration is in `configs/config.yaml` with QLoRA + Mistral-7B setup.

### Local Training
    
    # Or direct training
    accelerate launch -m axolotl.cli.train configs/config.yaml

### SLURM Training
    # Submit training job
    sbatch train.slurm
    
    # Monitor progress
    tail -f logs/almost-anselm-*.out

➡ Outputs:
- `models/base_v5/` (LoRA adapters)
- Training logs in `logs/`

---

## 🎯 Evaluation

- Shuffle test (real vs. bot responses)
- Human evaluation (chat quality, persona match)

## 📁 Project Structure

```
almost-anselm/
├── configs/
│   └── config.yaml              # Axolotl training config
├── data/
│   ├── raw/                     # Original Telegram exports
│   └── processed/               # Cleaned training data
├── docs/                        # Documentation
├── models/
│   ├── base_v5/                 # LoRA adapters
│   └── adapters/                # Model checkpoints
├── src/
│   ├── bot/
│   │   └── telegram_bot.py      # Telegram bot (v22+ API)
│   ├── data/
│   │   ├── build_dataset.py     # Data processing
│   │   ├── pull_telegram.py     # Message extraction
│   │   └── split_dataset.py     # Train/val/test split
│   └── inference/
│       ├── chat.py              # Enhanced interactive chat
│       ├── infer.py             # Basic inference
│       ├── merge.py             # LoRA merging
│       └── check_vllm.py        # vLLM testing
├── notebooks/
│   └── anselm_qLORA_train.ipynb # Training notebook
├── *.slurm                      # SLURM job scripts
└── logs/                        # Training/inference logs
```

### ⭐ Give a star if you like this project!


