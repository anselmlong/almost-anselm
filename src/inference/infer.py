from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model = "mistralai/Mistral-7B-v0.1"
lora_path = "/home/a/anselm/almost-anselm/models/base"  # your checkpoint folder

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

# 🚀 Load your LoRA adapter
model = PeftModel.from_pretrained(model, lora_path)

# (Optional) Merge lora weights for faster inference
# model = model.merge_and_unload()
model.eval()


def chat(prompt: str):
    formatted = f"<s>[INST] {prompt} [/INST]"
    inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=True,
            pad_token_id = tokenizer.eos_token_id,
            max_new_tokens=100,
            temperature=0.7,
            top_p=0.9
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chat(user_input)
        print("\nModel:", response)
