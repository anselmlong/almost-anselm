#!/usr/bin/env python3
"""
Stream-inspect a potentially large JSON array file like `data/processed/sft_train_new.json`.

Usage:
    python scripts/inspect_sft_json.py data/processed/sft_train_new.json --sample 5

What it does:
- Streams elements (works with very large files using `ijson` when available).
- Prints a pretty sample of the first N elements.
- Counts total elements and how many have a missing/empty `messages` field.
- Optionally writes the pretty sample to a file.

If `ijson` is not installed the script will attempt to load with the stdlib `json` (not suitable for huge files).
"""
import argparse
import json
import sys
from pathlib import Path


def stream_with_ijson(path):
    try:
        import ijson
    except Exception:
        return None
    f = open(path, "rb")
    return ijson.items(f, "item")


def stream_with_json(path):
    # fallback: load everything (may OOM on huge files)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        yield item


def inspect(path, sample_count=5, max_check=None, pretty_out=None):
    path = Path(path)
    if not path.exists():
        print("File not found:", path)
        return 2

    streamer = stream_with_ijson(path)
    if streamer is None:
        print("Warning: `ijson` not available, falling back to loading entire file (may be slow / memory heavy).\n"
              "Install ijson with `pip install ijson` for streaming support.")
        streamer = stream_with_json(path)

    total = 0
    missing_messages = 0
    samples = []

    for obj in streamer:
        total += 1
        if total <= sample_count:
            samples.append(obj)
        messages = obj.get("messages") if isinstance(obj, dict) else None
        if not messages:
            missing_messages += 1
        if max_check and total >= max_check:
            break

    print(f"Total examples checked: {total}")
    print(f"Examples with missing/empty 'messages': {missing_messages}")
    if samples:
        print(f"\nFirst {len(samples)} examples (pretty printed):\n")
        s = json.dumps(samples, indent=2, ensure_ascii=False)
        print(s)
        if pretty_out:
            with open(pretty_out, "w", encoding="utf-8") as out:
                out.write(s)
            print(f"\nWrote pretty sample to: {pretty_out}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="Path to JSON (array) or JSONL file")
    p.add_argument("--sample", type=int, default=5, help="How many examples to pretty-print")
    p.add_argument("--max-check", type=int, default=None, help="Max number of examples to scan (0 means unlimited)")
    p.add_argument("--pretty-out", default=None, help="Write pretty sample to this file")
    args = p.parse_args()

    return inspect(args.path, sample_count=args.sample, max_check=args.max_check, pretty_out=args.pretty_out)


if __name__ == "__main__":
    sys.exit(main())
