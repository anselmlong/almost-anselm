import json
import re
import hashlib
from dotenv import load_dotenv

load_dotenv()

WINDOW = 6
RAW_PATH = "../../data/raw/messages_clean.json"
OUT_PATH = "../../data/processed/cleaned_messages.json"

def normalize_text(text: str) -> str:
    # Mask obvious PII
    text = re.sub(r'\+?\d[\d\-\s]{7,}\d', '[PHONE]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    return text.strip()

def pseudo(sender_id: int, my_id: int) -> str:
    if sender_id == my_id:
        return "you"
    # Convert sender_id → stable pseudonym
    h = hashlib.sha256(str(sender_id).encode()).hexdigest()
    return f"user_{h[-4:]}"

def build_dataset():
    raw = json.load(open(RAW_PATH))
    my_id = next((m["sender_id"] for m in raw if m["is_out"]), None)

    samples = []
    for i in range(len(raw) - WINDOW):
        window = raw[i:i+WINDOW+1]
        target_msg = window[-1]

        if not target_msg["is_out"]:
            continue  # we only train on your replies

        # Build context dialogue
        ctx_lines = []
        for m in window[:-1]:
            role = pseudo(m["sender_id"], my_id)
            text = normalize_text(m["text"])
            if not text:
                continue
            ctx_lines.append(f"{role}: {text}")

        target_text = normalize_text(target_msg["text"])
        if not target_text:
            continue

        sample = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Anselm. Reply with your real tone and typical phrasing, based on past messages."
                },
                {
                    "role": "user",
                    "content": "\n".join(ctx_lines)
                }
            ],
            "output": target_text
        }
        samples.append(sample)

    json.dump(samples, open(OUT_PATH, "w"), ensure_ascii=False, indent=2)
    print(f"✅ Built {len(samples)} samples!")

if __name__ == "__main__":
    build_dataset()
