---
library_name: peft
license: apache-2.0
base_model: mistralai/Mistral-7B-v0.1
tags:
- axolotl
- base_model:adapter:mistralai/Mistral-7B-v0.1
- lora
- transformers
datasets:
- data/processed/sft_train_chatml.20k.jsonl
pipeline_tag: text-generation
model-index:
- name: models/base
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

[<img src="https://raw.githubusercontent.com/axolotl-ai-cloud/axolotl/main/image/axolotl-badge-web.png" alt="Built with Axolotl" width="200" height="32"/>](https://github.com/axolotl-ai-cloud/axolotl)
<details><summary>See axolotl config</summary>

axolotl version: `0.12.2`
```yaml
base_model: mistralai/Mistral-7B-v0.1
# optionally might have model_type or tokenizer_type
model_type: MistralForCausalLM
tokenizer_type: LlamaTokenizer
# Automatically upload checkpoint and final model to HF
# hub_model_id: username/custom_model_name

load_in_8bit: false
load_in_4bit: true

datasets:
  - path: data/processed/sft_train_chatml.20k.jsonl
    type: chat_template

    # step 1
    chat_template: chatml

    # step 2
    field_messages: messages
    message_property_mappings:
      role: role
      content: content

    roles:
      assistant:
        - system
        - gpt
        - model
        - assistant
      user:
        - human
        - user

    # step 3
    roles_to_train: ["assistant"]
    train_on_eos: "turn"

dataset_prepared_path: last_run_prepared
val_set_size: 0.1
output_dir: models/base 

adapter: qlora
lora_model_dir:

sequence_len: 1024
sample_packing: false


lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_linear: true
lora_target_modules:
  - gate_proj
  - down_proj
  - up_proj
  - q_proj
  - v_proj
  - k_proj
  - o_proj

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 8
micro_batch_size: 2
num_epochs: 1
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 0.0002

bf16: auto
tf32: false

gradient_checkpointing: true
resume_from_checkpoint:
auto_resume_from_checkpoints: true
logging_steps: 50
flash_attention: false

loss_watchdog_threshold: 5.0
loss_watchdog_patience: 3

warmup_ratio: 0.1
evals_per_epoch: 4
saves_per_epoch: 1
weight_decay: 0.0
special_tokens:

save_first_step: true  # uncomment this to validate checkpoint saving works with your config

```

</details><br>

# models/base

This model is a fine-tuned version of [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) on the data/processed/sft_train_chatml.20k.jsonl dataset.
It achieves the following results on the evaluation set:
- Loss: 5.7282
- Memory/max Mem Active(gib): 5.2
- Memory/max Mem Allocated(gib): 5.2
- Memory/device Mem Reserved(gib): 5.7

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0002
- train_batch_size: 2
- eval_batch_size: 2
- seed: 42
- gradient_accumulation_steps: 8
- total_train_batch_size: 16
- optimizer: Use OptimizerNames.ADAMW_BNB with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_steps: 112
- training_steps: 1124

### Training results

| Training Loss | Epoch  | Step | Validation Loss | Mem Reserved(gib) | Mem Active(gib) | Mem Allocated(gib) |
|:-------------:|:------:|:----:|:---------------:|:-----------------:|:---------------:|:------------------:|
| No log        | 0      | 0    | 4.6652          | 7.04              | 6.62            | 6.62               |
| 4.6527        | 0.0001 | 1    | 4.6459          | 5.7               | 5.2             | 5.2                |
| 6.5029        | 0.2567 | 577  | 5.7282          | 5.2               | 5.2             | 5.7                |


### Framework versions

- PEFT 0.17.0
- Transformers 4.55.2
- Pytorch 2.6.0+cu124
- Datasets 4.0.0
- Tokenizers 0.21.4
