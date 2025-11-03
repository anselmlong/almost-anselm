import json, os, random
from datetime import datetime
from collections import defaultdict

IN_PATH = "../../data/processed/cleaned_messages.json"
OUT_DIR = "../../data/processed"
TRAIN_OUT = os.path.join(OUT_DIR, "sft_train.json")
VAL_OUT   = os.path.join(OUT_DIR, "sft_val.json")
TEST_OUT  = os.path.join(OUT_DIR, "sft_test.json")

RNG_SEED = 42
SPLITS = (0.90, 0.05, 0.05)  # train / val / test
TIME_SPLIT = True            # set False to use grouped random
TEST_IS_MOST_RECENT = True   # when TIME_SPLIT=True, put the most recent chunk into test

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
    n_val = int(SPLITS[1] * n)
    n_test = n - n_train - n_val

    if TEST_IS_MOST_RECENT:
        train = with_ts[:n_train]
        val   = with_ts[n_train:n_train+n_val]
        test  = with_ts[n_train+n_val:]
    else:
        # contiguous chronological blocks anyway
        train = with_ts[:n_train]
        val   = with_ts[n_train:n_train+n_val]
        test  = with_ts[n_train+n_val:]

    # append the timestamp-missing samples to train (or distribute if you prefer)
    train += without_ts
    return train, val, test

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

    train, val, test = [], [], []
    n_total = len(samples)
    n_train = int(SPLITS[0] * n_total)
    n_val   = int(SPLITS[1] * n_total)
    n_test = n_total - n_train - n_val
    # Fill by whole groups to avoid leakage
    for _, grp in groups:
        # Place full groups into train/val/test in order until targets reach their sizes.
        # Use per-split thresholds (not cumulative thresholds) to avoid overfilling the test split.
        if len(train) < n_train:
            train.extend(grp)
        elif len(val) < n_val:
            val.extend(grp)
        else:
            test.extend(grp)

    # Distribute unknowns deterministically
    for i, s in enumerate(unknown_bucket):
        if len(train) < n_train:
            train.append(s)
        elif len(val) < n_val:
            val.append(s)
        else:
            test.append(s)

    return train, val, test

def main():
    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Optional: sanity check on size
    print(f"Loaded {len(data)} samples")

    if TIME_SPLIT:
        train, val, test = time_based_split(data)
    else:
        train, val, test = grouped_random_split(data)

    # Trim if rounding pushed over
    total = len(train) + len(val) + len(test)
    print(f"Split sizes → train={len(train)}, val={len(val)}, test={len(test)} (total {total})")

    write_json(TRAIN_OUT, train)
    write_json(VAL_OUT, val)
    write_json(TEST_OUT, test)
    print(f"✅ Saved:\n  {TRAIN_OUT}\n  {VAL_OUT}\n  {TEST_OUT}")

if __name__ == "__main__":
    main()
