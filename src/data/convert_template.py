import json
import pathlib

INPUT_PATH = pathlib.Path("data/processed/sft_val.json")
OUTPUT_PATH = pathlib.Path("data/processed/sft_val_chatml.jsonl")

def convert_sample(original):
    # Expect original format:
    # {
    #   "messages": [
    #     {"role":"system", "content": "..."},
    #     {"role":"user",   "content": "..."}
    #   ],
    #   "output": "<assistant reply>"
    # }
    msgs = original.get("messages", [])
    output = original.get("output", "").strip()
    if not output:
        raise ValueError("No output field in sample: {}".format(original))
    # Append assistant turn
    msgs.append({
        "role": "assistant",
        "content": output
    })
    # Build new sample
    return {
        "messages": msgs
    }

def main():
    print("Reading from:", INPUT_PATH)
    with open(INPUT_PATH, "r", encoding="utf-8") as f_in:
        text = f_in.read().strip()

    # Determine whether input is a JSON array (single-file) or JSONL (one JSON object per line)
    samples = []
    if not text:
        print("Input file is empty:", INPUT_PATH)
        return

    try:
        data = json.loads(text)
        # If the file contains a top-level list, treat each element as a sample
        if isinstance(data, list):
            samples = data
        elif isinstance(data, dict):
            # single dict: maybe one sample
            samples = [data]
        else:
            raise ValueError("Unexpected JSON root type: {}".format(type(data)))
    except json.JSONDecodeError:
        # Fallback: try to parse as JSONL (one JSON object per line)
        samples = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            samples.append(json.loads(line))

    # Convert and write out as JSONL
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        for original in samples:
            # If the parsed element itself is a list (unexpected), skip or handle
            if isinstance(original, list):
                # assume it's a list of messages already
                sample_obj = {"messages": original}
                try:
                    new_sample = convert_sample(sample_obj)
                except Exception as e:
                    print("Skipping element (list) due to:", e)
                    continue
            else:
                try:
                    new_sample = convert_sample(original)
                except Exception as e:
                    print("Skipping sample due to:", e)
                    continue

            f_out.write(json.dumps(new_sample, ensure_ascii=False) + "\n")

    print("Wrote converted file to:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
