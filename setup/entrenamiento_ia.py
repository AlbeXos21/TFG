
from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
from unsloth.chat_templates import train_on_responses_only
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq

import torch

# Load your model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length= 2048, 
    dtype=None,
    load_in_4bit=True,
)


# Load dataset
dataset = load_dataset("csv", data_files="./imdb_sup.csv")

# Format training dataset
def format_train_template(row):
    row_json = [
        {"role": "user", "content": row["Review"]},
        {"role": "assistant", "content": row["Rating"]}
    ]
    # Apply chat template and ensure truncation is handled
    row["text"] = tokenizer.apply_chat_template(row_json, tokenize=False)
    return row

dataset = dataset["train"].map(
    format_train_template,
    num_proc=4,
)
dataset = dataset.train_test_split(test_size=0.1)

# Adjust the model with PEFT (parameter-efficient fine-tuning)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,  # Dropout setting
    bias="none",  # Bias handling
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

# Initialize the trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,  # Removed max_seq_length from here
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
    args=TrainingArguments(
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
        report_to="none",
    ),
)

# Use a custom function to handle response-based training
trainer = train_on_responses_only(
    trainer,
    instruction_part="<|start_header_id|>user<|end_header_id|>\n\n",
    response_part="<|start_header_id|>assistant<|end_header_id|>\n\n",
)

# Train the model
trainer_stats = trainer.train()
print(trainer_stats)

# Save the model and tokenizer after training
model.save_pretrained("Llama-3.2-3B-ReviewsFineTuning")
tokenizer.save_pretrained("Llama-3.2-3B-ReviewsFineTuning")
