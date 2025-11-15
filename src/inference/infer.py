from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model = "mistralai/Mistral-7B-v0.1"
lora_path = "/home/a/anselm/almost-anselm/models/base"  # your checkpoint folder

# Using mistral tokenizer
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
    formatted_string = tokenizer.apply_chat_template(prompt, tokenize=False)
    token_ids = tokenizer.apply_chat_template(formatted_string, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **token_ids,
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
