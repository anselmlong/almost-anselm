import json
import re
import hashlib
from dotenv import load_dotenv
from pathlib import Path
from typing import Union, List, Any

load_dotenv()

WINDOW = 6
RAW_PATH = "../../data/raw/messages.json"
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
    raw = load_json_robust(RAW_PATH)
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
        print (f"Sample {i} out of {len(raw) - WINDOW}: {ctx_lines} -> {target_text}")

    json.dump(samples, open(OUT_PATH, "w"), ensure_ascii=False, indent=2)
    print(f"✅ Built {len(samples)} samples!")

def load_json_robust(path: Union[str, Path], *, allow_ndjson: bool = True, replace_invalid: bool = False) -> Any:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    # Read with UTF-8, optionally replace invalid bytes rather than raising
    errors = "replace" if replace_invalid else "strict"
    text = p.read_text(encoding="utf-8", errors=errors)

    # Strip BOM if present
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    text = text.strip()
    if not text:
        raise ValueError(f"Empty JSON file: {p}")

    # Try normal JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If NDJSON (newline-delimited), parse each non-empty line
        if allow_ndjson:
            lines = [ln for ln in text.splitlines() if ln.strip()]
            if not lines:
                raise
            try:
                return [json.loads(ln) for ln in lines]
            except Exception:
                # If even NDJSON parsing failed, re-raise original exception
                raise
        raise

if __name__ == "__main__":
    build_dataset()
