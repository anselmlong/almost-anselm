import random
import sys
from pathlib import Path
from typing import List

#!/usr/bin/env python3
"""
scale_down.py

Randomly sample K lines from a JSONL file using reservoir sampling (memory O(K)).
Usage:
	python scale_down.py --input sft_train_chatml.jsonl --output sft_train_chatml.20k.jsonl --k 20000 --seed 42
"""



def reservoir_sample_lines(path: Path, k: int, seed: int | None = None) -> List[str]:
	rng = random.Random(seed)
	reservoir: List[str] = []
	with path.open("r", encoding="utf-8") as f:
		for i, line in enumerate(f):
			if not line.strip():
				continue  # skip empty lines
			if i < k:
				reservoir.append(line)
			else:
				j = rng.randint(0, i)
				if j < k:
					reservoir[j] = line
	return reservoir


def main() -> None:
	# Hardcoded parameters (edit these values as needed)
	INPUT_PATH = Path("data/processed/sft_train_chatml.jsonl")
	OUTPUT_PATH = Path("data/processed/sft_train_chatml.20k.jsonl")
	K = 20000
	SEED = 42
	SHUFFLE_OUTPUT = True

	input_path = INPUT_PATH
	if not input_path.exists():
		print(f"Input file not found: {input_path}", file=sys.stderr)
		sys.exit(2)

	out_path = OUTPUT_PATH
	samples = reservoir_sample_lines(input_path, K, SEED)

	if not samples:
		print("No samples found in input file.", file=sys.stderr)
		sys.exit(3)

	rng = random.Random(SEED)
	if SHUFFLE_OUTPUT:
		rng.shuffle(samples)

	# If input had fewer than K lines, inform user
	if len(samples) < K:
		print(f"Input had only {len(samples)} valid non-empty lines; writing all of them to {out_path}", file=sys.stderr)

	with out_path.open("w", encoding="utf-8") as out_f:
		out_f.writelines(samples)

	print(f"Wrote {len(samples)} lines to {out_path}")


if __name__ == "__main__":
	main()