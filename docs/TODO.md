# 📌 Project TODO — Telegram Persona LLM (“Anselm AI”)

This checklist tracks the full pipeline from Telegram export → persona fine-tuning → bot → preference RL reinforcement.

---

## ✅ Phase 0 — Repo & Environment

- [X] Clone repository + set up folder structure
- [X] Create Python virtual env (`python -m venv venv`)
- [X] Install dependencies (`pip install -r requirements.txt`)
- [X] Fill in `.env` using `.env.example` template
  - [X] `TG_API_ID`, `TG_API_HASH` (Telegram)
  - [ ] `BOT_TOKEN` (Telegram BotFather)
  - [ ] `HF_TOKEN` (Hugging Face, optional)

---

## 📥 Phase 1 — Data Collection

- [X] Use `pull_telegram.py` to fetch cloud messages
  - [X] Limit message scope (DMs, selected groups)
- [X] Validate message quality: fields present (text, timestamp, sender etc.)
- [X] Store raw data in `data/raw/messages.json`

---

## 🛁 Phase 2 — Data Cleaning & Anonymization

- [ ] Implement `build_dataset.py`:
  - [ ] Replace other users’ identifiers with pseudonyms (`user_XXXX`)
  - [ ] Remove or mask:
    - PII (phone, email)
    - Sensitive URLs
- [ ] Filter messages:
  - [ ] Remove media-only messages
  - [ ] Optional: Keep emoji-only replies if stylistic
- [ ] Re-save cleaned dataset: `data/raw/messages_clean.json`

---

## 🧩 Phase 3 — Dataset Construction for SFT

- [ ] Implement windowed pairing (context → your reply)
  - [ ] Choose window size (default: 6–10 exchanges)
- [ ] Add system prompt indicating style + persona
- [ ] Split into:
  - [ ] train (80%)
  - [ ] val (10%)
  - [ ] test (10%) by thread ID
- [ ] Save final formatted dataset → `data/processed/sft_data.json`
- [ ] Create dataset stats (count, avg length, distribution)

---

## 🧪 Phase 4 — Baseline Inference (No Training)

- [ ] Try out inference using:
  - [ ] Base model (e.g., Mistral-7B or Llama3-8B)
  - [ ] Very light prompt engineering using real examples
- [ ] Evaluate initial style closeness qualitatively

🚀 This sets a baseline before fine-tuning.

---

## 🧠 Phase 5 — Fine-Tuning (QLoRA SFT)

- [ ] Configure `axolotl_config.yaml` with dataset paths + LoRA params
- [ ] Train using Axolotl:
  - [ ] Monitor loss + early stop if needed
- [ ] Save LoRA adapters → `models/adapters/`
- [ ] Merge adapter with base model for runtime
- [ ] Validate on hold-out samples:
  - Did tone/style match yours?
  - Any hallucinations or inappropriate replies?

---

## 🔍 Phase 6 — Retrieval Augmentation

- [ ] Build vector store (`FAISS`) in `data/embeddings/`
- [ ] Index:
  - Past messages
  - Persona anchors (example replies)
- [ ] Implement retrieval ranking in `retrieval_pipeline.py`:
  - [ ] Top-k similarity search (`k=3–5`)
  - [ ] Prompt template includes recent chat history + retrieved examples
- [ ] Integration test → drastically improves realism

---

## 🤖 Phase 7 — Telegram Bot Deployment

- [ ] Implement `/start` + message handler (`telegram_bot.py`)
- [ ] Connect to local inference server (vLLM/Ollama)
- [ ] Track conversational memory per user
- [ ] Add safety guardrails:
  - [ ] Block or warn on secrets
  - [ ] Max tokens/time limits
- [ ] Beta test with friends

---

## 🎯 Phase 8 — Evaluation

- [ ] A/B test: real answer vs bot answer (shuffled)
- [ ] Style classifier:
  - ✅ classify: “Anselm vs. Generic AI”
- [ ] Track metrics:
  - Accuracy
  - Response quality (manual labels)
  - Latency

---

## ⚙️ Phase 9 — Preference Fine-Tuning (DPO/KTO)

- [ ] Activate preference feedback UI:
  - ✅ “Yes, I’d respond like that”
  - ❌ “Not like me”
- [ ] Collect dataset of preference pairs or ratings
- [ ] Implement DPO pass (`run_dpo.py`)
  - [ ] Re-fine-tune model using reward-aligned preference data
- [ ] Deploy updated bot
- [ ] Continuous updates as new data arrives

---

## 🔐 Phase 10 — Privacy / Governance

- [ ] `/forget` command to delete conversation memory for any user
- [ ] Clearly disclose bot is an AI persona
- [ ] Store raw message exports locally only
- [ ] (Optional) Publish **LoRA adapter only** for safety

---

## 🛣️ Future Ideas

- [ ] Online RL with bounded exploration
- [ ] Emotion-aware responses
- [ ] Voice clone integration (TTS + style conditioning)
- [ ] Multi-persona mode (e.g. “Professional Anselm”, “Casual Anselm”)
- [ ] Web UI dashboard to manage training loops & memory store

---

### ✅ Progress Summary Table

| Phase | Status | Notes |
|-------|--------|------|
| 0 — Env Setup | ⬜ | |
| 1 — Data Pull | ⬜ | |
| 2 — Cleaning | ⬜ | |
| 3 — SFT Dataset | ⬜ | |
| 4 — Baseline Inference | ⬜ | |
| 5 — QLoRA SFT | ⬜ | |
| 6 — Retrieval | ⬜ | |
| 7 — Telegram Bot | ⬜ | |
| 8 — Evaluation | ⬜ | |
| 9 — RL (DPO) | ⬜ | |
| 10 — Privacy | ⬜ | |
