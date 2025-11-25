from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

import time

base_model_name = "mistralai/Mistral-7B-v0.1"
adapter_path = "./models/base_v4"  # path to your LoRA adapter

print("[1/5] Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype="auto",  # or torch.float16 if you're sure your GPU supports it
    load_in_4bit=True,
    device_map="auto"
)

print("[2/5] Loading LoRA adapter...")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("[3/5] Merging adapter with base model...")
start = time.time()
model = model.merge_and_unload()
print(f"[4/5] Merge complete in {time.time() - start:.2f} seconds.")

output_path = "./merged_model"
print(f"[5/5] Saving merged model to {output_path}...")
model.save_pretrained(output_path)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
tokenizer.save_pretrained(output_path)

print("✅ All done. You can now upload to Hugging Face or use with vLLM.")

