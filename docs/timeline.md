| Phase                        | Description                  | Time          | Notes                         |
| ---------------------------- | ---------------------------- | ------------- | ----------------------------- |
| 0 — Setup                    | Repo, README, venv, tokens   | **0.5–1 day** | Already partly done ✅         |
| 1 — Data Collection          | Telethon pull, testing       | **1–2 days**  | Depends on volume + debugging |
| 2 — Cleaning & Anonymization | PII removal + formatting     | **1–2 days**  | Iterative tuning              |
| 3 — Dataset Prep             | Windowing, splits, stats     | **1 day**     | Testing sample quality        |
| 4 — Baseline Inference       | No-train persona prompting   | **0.5 day**   | Needed for comparison         |
| 5 — QLoRA Fine-Tune          | Training run + validation    | **2–4 days**  | Includes 1–2 GPU runs         |
| 6 — Retrieval Augmentation   | FAISS + inference pipeline   | **2–3 days**  | Debug prompt structure        |
| 7 — Telegram Bot             | Deployment + memory store    | **2 days**    | UX details                    |
| 8 — Evaluation               | A/B tests + metrics          | **1 day**     | Human feedback                |
| 9 — DPO/KTO RL Tuning        | Pref UI + training pass      | **3–5 days**  | Data collection needed        |
| 10 — Privacy & Safety        | `/forget`, disclaimers, logs | **0.5–1 day** | Low effort                    |
