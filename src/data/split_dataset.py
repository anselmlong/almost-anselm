import json, os, random
from datetime import datetime
from collections import defaultdict

from pathlib import Path

# Resolve paths from repo root (so script can be run from any CWD)
REPO_ROOT = Path(__file__).resolve().parents[2]
IN_PATH = REPO_ROOT / "data" / "processed" / "cleaned_messages.jsonl"
OUT_DIR = REPO_ROOT / "data" / "processed"
TRAIN_OUT = OUT_DIR / "sft_train_new.json"
VAL_OUT = OUT_DIR / "sft_val_new.json"

RNG_SEED = 42
SPLITS = (0.90, 0.10)  # train / val
TIME_SPLIT = False         # set False to use grouped random
TEST_IS_MOST_RECENT = True   # retained but test set will be discarded; most-recent logic kept for val ordering

def parse_ts(sample):
    # Expect ISO timestamp at sample["metadata"]["timestamp"] or ["timestamp"]
    meta = sample.get("metadata", {})
    ts = meta.get("timestamp") or sample.get("timestamp")
    if not ts:
        return None
    try:
        # Handle both naive and tz-aware
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if "Z" in ts else datetime.fromisoformat(ts)
        return dt
    except Exception:
        return None

def get_chat_id(sample):
    meta = sample.get("metadata", {})
    return meta.get("chat_id") or sample.get("chat_id")

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def time_based_split(samples):
    # Require timestamps; fall back if missing
    with_ts = [s for s in samples if parse_ts(s) is not None]
    without_ts = [s for s in samples if parse_ts(s) is None]

    if len(with_ts) < int(0.8 * len(samples)):
        print("⚠️ Not enough timestamps to do robust time split. Falling back to grouped random.")
        return grouped_random_split(samples)

    # Sort by time
    with_ts.sort(key=lambda s: parse_ts(s))
    n = len(with_ts)
    n_train = int(SPLITS[0] * n)
    # Put the remainder into val so train+val == n
    n_val = n - n_train

    if TEST_IS_MOST_RECENT:
        train = with_ts[:n_train]
        val   = with_ts[n_train:]
    else:
        train = with_ts[:n_train]
        val   = with_ts[n_train:]

    # append the timestamp-missing samples to train (or distribute if you prefer)
    train += without_ts
    return train, val

def grouped_random_split(samples):
    random.seed(RNG_SEED)
    # Group by chat_id if available to reduce leakage
    buckets = defaultdict(list)
    unknown_bucket = []
    for s in samples:
        cid = get_chat_id(s)
        if cid is None:
            unknown_bucket.append(s)
        else:
            buckets[cid].append(s)

    groups = list(buckets.items())
    random.shuffle(groups)

    train, val = [], []
    n_total = len(samples)
    n_train = int(SPLITS[0] * n_total)
    # ensure all samples accounted for
    n_val   = n_total - n_train
    # Fill by whole groups to avoid leakage
    for _, grp in groups:
        # Place full groups into train/val/test in order until targets reach their sizes.
        # Use per-split thresholds to avoid leakage. Fill train first, then val.
        if len(train) < n_train:
            train.extend(grp)
        else:
            val.extend(grp)

    # Distribute unknowns deterministically
    for i, s in enumerate(unknown_bucket):
        if len(train) < n_train:
            train.append(s)
        else:
            val.append(s)

    return train, val

def main():
    # Support both JSON array and JSONL input
    with open(IN_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try NDJSON / JSONL: one JSON object per line
        data = [json.loads(line) for line in text.splitlines() if line.strip()]

    # Optional: sanity check on size
    print(f"Loaded {len(data)} samples")

    if TIME_SPLIT:
        train, val = time_based_split(data)
    else:
        train, val = grouped_random_split(data)

    # Trim if rounding pushed over
    total = len(train) + len(val)
    print(f"Split sizes → train={len(train)}, val={len(val)} (total {total})")

    write_json(TRAIN_OUT, train)
    write_json(VAL_OUT, val)
    print(f"✅ Saved:\n  {TRAIN_OUT}\n  {VAL_OUT}")

if __name__ == "__main__":
    main()
