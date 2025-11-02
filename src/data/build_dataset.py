"""Build SFT-ready dataset from processed messages.

This script should load anonymized messages and emit training samples.
"""

import json
from pathlib import Path
from typing import List, Dict


def build_dataset(processed_dir: str, out_file: str) -> None:
    """Create a very small example dataset file.

    Args:
        processed_dir: directory with processed JSON files
        out_file: output .jsonl file path
    """
    p = Path(processed_dir)
    # Placeholder: gather all .json files and write simple samples
    samples: List[Dict] = []
    for f in p.glob("*.json"):
        try:
            data = json.load(f.open())
            samples.append({"input": data.get("text", ""), "output": ""})
        except Exception:
            continue

    with open(out_file, "w") as fh:
        for s in samples:
            fh.write(json.dumps(s) + "\n")


if __name__ == "__main__":
    print("Placeholder: run build_dataset(processed_dir, out_file)")
