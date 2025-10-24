import os
import argparse
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

def main():
    # 1. Argument parsing for input data
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_data", type=str, help="Path to input data (file or folder)")
    args = parser.parse_args()

    # 2. Load and prepare dataset
    dataset = load_dataset('json', data_files=os.path.join(args.data_dir, 'training_data.jsonl'), split='train')

    # 3. Model and tokenizer setup
    model_name = "mistralai/Mistral-7B-v0.1" # or another model from the Hugging Face catalog

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=False,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map={"": 0}
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # 4. PEFT configuration (LoRA)
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, peft_config)

    # 5. Training arguments
    training_arguments = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=10,
        logging_steps=10,
        learning_rate=2e-4,
        fp16=True,
        max_steps=50,
    )

    # 6. SFTTrainer setup
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="prompt",
        tokenizer=tokenizer,
        args=training_arguments,
        packing=False,
    )

    # 7. Start training
    trainer.train()

    # 8. Save the final model
    trainer.model.save_pretrained("fine_tuned_model")
    tokenizer.save_pretrained("fine_tuned_model")

if __name__ == "__main__":
    main()
