almost-anselm/
│
├─ data/
│   ├─ raw/               # Telethon raw message dumps
│   ├─ processed/         # Cleaned, anonymized dataset
│   └─ embeddings/        # Vector store for retrieval
│
├─ src/
│   ├─ data/
│   │   ├─ pull_telegram.py      # Extract messages via Telethon
│   │   ├─ anonymize.py          # Replace names, redact PII
│   │   └─ build_dataset.py      # Create SFT-ready samples
│   │
│   ├─ train/
│   │   ├─ axolotl_config.yaml   # QLoRA config
│   │   └─ run_sft.sh            # Training launcher
│   │
│   ├─ inference/
│   │   ├─ serve_model.py        # vLLM / Ollama / HF inference server
│   │   ├─ embed_store.py        # FAISS vector store creation + search
│   │   └─ retrieval_pipeline.py # Build prompt w/ memory + examples
│   │
│   ├─ bot/
│   │   ├─ telegram_bot.py       # Telegram handler + RL UI
│   │   └─ bot_memory.py         # Store per-user chat history
│   │
│   ├─ rl/
│   │   ├─ collect_prefs.py      # Logging + UI for feedback
│   │   └─ run_dpo.py            # Offline preference tuning
│   │
│   └─ utils/
│       ├─ logging.py
│       └─ config.py
│
├─ models/
│   ├─ base/                      # e.g. Llama-3-8B-Instruct weights (local)
│   └─ adapters/                  # LoRA adapters after training
│
├─ .env.example                   # API tokens placeholder
├─ requirements.txt               # Python deps
└─ README.md                      # Setup + instructions
