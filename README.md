# 🤖 Anselm AI — Telegram Persona LLM

A Telegram bot fine-tuned on my real conversation style, capable of chatting like me and continually improving via reinforcement feedback.

**Note: This README is generated with AI tools. Will be refined as the project goes along.**

---

## 🚀 Overview

Pipeline:
1. ✅ Pull Telegram messages (your side of conversations)
2. ✅ Clean + anonymize data
3. ✅ Build supervised training dataset (context → your reply)
4. ✅ Fine-tune a 7B model with QLoRA
5. ✅ Add retrieval of similar past messages
6. ✅ Deploy as a Telegram bot that chats like you
7. ✅ RL preference tuning (“Would I reply like that?”)

---

## 🧱 Tech Stack

| Component | Tool |
|---------|------|
| LLM Base | Mistral-7B-Instruct / Llama-3-8B-Instruct |
| Fine-tuning | Axolotl + QLoRA |
| Vector Store | FAISS |
| Telegram Integration | Telethon + python-telegram-bot |
| Inference | vLLM / Ollama |
| Preferences | DPO / KTO |

---

## 📦 Setup & Installation

### 1️⃣ Clone Repo
    git clone https://github.com/yourusername/telegram-anselm-ai.git
    cd telegram-anselm-ai

### 2️⃣ Create Virtual Environment
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows

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

## 🛁 Anonymize & Clean

    python anonymize.py

➡ Output: `data/raw/messages_clean.json`

---

## 📐 Dataset for SFT

    python build_dataset.py

➡ Output: `data/processed/sft_data.json`

---

## 🧪 Baseline Test (without training)

Try inference with base model + prompt examples to establish style baseline.

---

## 🧠 QLoRA Fine-Tuning

Ensure `axolotl_config.yaml` is configured correctly → dataset & LoRA params

    cd src/train
    bash run_sft.sh

➡ Outputs:
`models/adapters/` (LoRA adapters)

---

## 🔍 Retrieval Augmentation

    cd src/inference
    python embed_store.py

Bot now retrieves semantically similar past messages → more realistic style

---

## 🤖 Telegram Bot Deployment

    cd src/bot
    python telegram_bot.py

Talk with your AI persona in Telegram 🎉

---

## 🎯 Evaluation

- Shuffle test (real vs. bot responses)
- Classifier: “Anselm vs. Generic AI”
- Track:
  - Latency
  - Hallucination rate
  - Conversation quality

---

## ⚙️ RL Preferences: DPO / KTO

Collect preference feedback:

    python ../rl/collect_prefs.py

Refine model:

    python ../rl/run_dpo.py

Republish updated persona — improves over time 🚀

---

## 🔐 Privacy & Safety

✔ Raw data stays local  
✔ Other users are anonymized  
✔ Add `/forget` to erase memory for any user  
✔ Bot clearly states it is an AI version of Anselm

---

## ✅ Progress Tracker

See: **TODO.md**

---

## 🙌 Contributing

PRs welcome — especially around:
- anonymization,
- evaluation,
- safety tooling.

---

### ⭐ Give a star if you like this project!

--- 

## References

https://medium.com/data-science-collective/i-fine-tuned-an-llm-on-5-years-of-telegram-chats-7bacb66387c8
