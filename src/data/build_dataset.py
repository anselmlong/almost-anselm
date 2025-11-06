import json
import re
import math
from dotenv import load_dotenv
from pathlib import Path
from typing import Union, List, Any, Optional
from datetime import datetime

load_dotenv()

# Time window (seconds) and token budget per group
TIME_WINDOW_SECONDS = 10 * 60  # 10 minutes
MAX_TOKENS = 768

# Paths (edit as needed)
# Resolve paths relative to repository root so running the script from any CWD works
REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = REPO_ROOT / "data" / "raw" / "messages.json"
OUT_PATH = REPO_ROOT / "data" / "processed" / "cleaned_messages.json"
MY_ID = 495290408

def normalize_text(text: str) -> str:
    # Mask obvious PII
    text = re.sub(r'\+?\d[\d\-\s]{7,}\d', '[PHONE]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    return text.strip()


def pseudo(sender_id: int, my_id: int) -> str:
    if sender_id == my_id:
        return "assistant"
    # Convert sender_id → stable pseudonym
    return "user"


def _parse_date(v) -> float:
    """Return timestamp in seconds (float). Accept epoch (int/float) or ISO string."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            # datetime.fromisoformat handles many ISO forms
            dt = datetime.fromisoformat(v)
            return dt.timestamp()
        except Exception:
            # Try integer parse
            try:
                return float(v)
            except Exception:
                raise ValueError(f"Unrecognized date format: {v}")
    raise ValueError(f"Unsupported date type: {type(v)}")


def _token_count(text: str) -> int:
    """Estimate token count. Prefer tiktoken if available, else fallback to simple heuristic."""
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        # Fallback: conservative estimate: token ~= words * 1.3, at least 1
        words = len(text.split())
        return max(1, math.ceil(words * 1.3))


def group_by_time_and_tokens(raw: List[dict], time_window_seconds: int = TIME_WINDOW_SECONDS, max_tokens: int = MAX_TOKENS) -> List[List[dict]]:
    """Group messages into contiguous chunks where consecutive messages are within `time_window_seconds`
    and total tokens in the group do not exceed `max_tokens`.

    raw: list of message dicts with at least keys: 'date' (epoch or ISO), 'text', 'is_out', 'sender_id'
    Returns a list of groups (each group is a list of messages in chronological order).
    """
    # Sort by timestamp ascending
    items = sorted(raw, key=lambda m: _parse_date(m.get("date")))

    groups: List[List[dict]] = []
    cur_group: List[dict] = []
    cur_tokens = 0
    prev_ts: Optional[float] = None

    for m in items:
        try:
            ts = _parse_date(m.get("date"))
        except Exception:
            # If no parseable date, treat as separate message far apart
            ts = None

        text = normalize_text(m.get("text", "") or "")
        if not text:
            # Skip empty messages entirely
            continue

        tcount = _token_count(text)

        # Determine if we should start a new group
        start_new = False
        if prev_ts is None:
            start_new = True
        else:
            if ts is None or (ts - prev_ts) > time_window_seconds:
                start_new = True
            elif cur_tokens + tcount > max_tokens:
                start_new = True

        if start_new:
            if cur_group:
                groups.append(cur_group)
            cur_group = [m]
            cur_tokens = tcount
        else:
            cur_group.append(m)
            cur_tokens += tcount

        prev_ts = ts if ts is not None else prev_ts

    if cur_group:
        groups.append(cur_group)

    return groups


def build_dataset():
    raw = load_json_robust(RAW_PATH)
    my_id = MY_ID
    
    groups = group_by_time_and_tokens(raw)
    samples = []

    for gi, group in enumerate(groups):
        # We only create a sample when the last message in the group is an outgoing message
        last = group[-1]
        if not last.get("is_out"):
            continue

        # Build context: all messages before the last one
        convo = []
        for m in group:
            reply = {}
            role = pseudo(m.get("sender_id"), my_id)
            text = normalize_text(m.get("text", "") or "")
            if not text:
                continue
            reply["role"] = role
            reply["content"] = text
            convo.append(reply)
        # Sample format: {"messages": [{"role": "...", "content": "..."}, ...]}
        # convo is already a list of message dicts, so use it directly
        samples.append({"messages": convo})
        print(f"Group {gi} ({len(group)} msgs): {convo}")

    out_p = Path(OUT_PATH)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(samples, open(out_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ Built {len(samples)} samples!")

def load_json_robust(path: Union[str, Path], *, allow_ndjson: bool = True, replace_invalid: bool = False) -> Any:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON input file not found: {p}\nPlease create or export your Telegram pull to this path, or edit `RAW_PATH` in this script to point to your messages file.")

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
