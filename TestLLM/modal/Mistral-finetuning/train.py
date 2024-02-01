from datetime import datetime
from modal import Secret, gpu, Mount
from transformers import TrainerCallback
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shared import stub, BASE_MODEL, MODEL_DIR, VOLUME_CONFIG

WANDB_PROJECT = "hf-mistral7b-finetune"
# N_GPUS = int(os.environ.get("N_GPUS", 2))
# GPU_MEM = int(os.environ.get("GPU_MEM", 80))
GPU_CONFIG = gpu.A100(memory=80, count=4)

# Callback to store model checkpoints in modal.volume
class CheckpointCallback(TrainerCallback):
    def __init__(self, volume):
        self.volume = volume

    def on_save(self, args, state, control, **kwargs):
        if state.is_world_process.zero:
            print("Running commit on modal.Volume after model checkpoint")
            self.volume.commit()


#Load data to modal volume
@stub.function(volumes=VOLUME_CONFIG,
            mounts=[Mount.from_local_dir("../../../data", remote_path="/root"),])
def load_dataset():
    # import os
    import pandas as pd

    def format_instruction(sample):
        PROMPT_TEMPLATE = "[INST] <<SYS>>\nUse the Input to provide a response from a question about medical domain.\n<</SYS>>\n\nInput:\n{user} [/INST]\n\nResponse: {assistant}"
        return {"text": PROMPT_TEMPLATE.format(user=sample["user"], assistant=sample["assistant"])}  

    train_dataset = pd.read_csv('training_data.csv')
    val_dataset = pd.read_csv('validating_data.csv')


    train_dataset = train_dataset.apply(format_instruction, axis=1)
    val_dataset = val_dataset.apply(format_instruction, axis=1)

    train_dataset.to_json("train_data.jsonl", orient='records', lines=True)
    val_dataset.to_json("val_data.jsonl",orient='records', lines=True)

    stub.training_data_volume.commit()


# define finetune function
@stub.function(gpu=GPU_CONFIG,
               secret=Secret.from_name("my-wandb-secret-2") if WANDB_PROJECT else None,
               timeout=60*60*4,
               volumes=VOLUME_CONFIG)
def finetune(model_name:str, run_id:str="", wandb_project: str = "", resume_from_checkpoint: str = None):
    import os
    import torch
    import transformers
    from peft import (
        LoraConfig,
        get_peft_model,
        prepare_model_for_kbit_training,
        set_peft_model_state_dict
        )
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    #rom ctransformers import AutoModelForCausalLM #use AutoTokenizer here
    from datasets import load_dataset


    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, quantization_config=bnb_config)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

    def tokenize(sample, cutoff_len=512, add_eos_token=True):
        prompt = sample["text"]
        result = tokenizer.__call__(
            prompt,
            truncation=True,
            max_length=cutoff_len,
            padding="max_length"
        )
        if(
            result['input_ids'][-1] != tokenizer.eos_token_id
            and len(result['input_ids']) < cutoff_len
            and add_eos_token
        ):
            result['input_ids'].append(tokenizer.eos_token_id)
            result['attention_mask'].append(1)
        result['labels'] = result['input_ids'].copy()

        return result

    # Load datasets from training data Volume
    train_dataset = load_dataset("csv", data_files="/training_data/train_data.csv", split="train")
    eval_dataset = load_dataset("csv", data_files="/training_data/val_data.csv", split="train")

    # tokenize data
    tokenized_train_dataset = train_dataset.map(tokenize)
    tokenized_val_dataset = eval_dataset.map(tokenize)

    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)

    congig = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
            "lm_head"
        ],
        bias="none",
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, congig)

    if len(wandb_project) > 0:
        # Set environment variables if Weights and Biases is enabled
        os.environ["WANDB_PROJECT"] = wandb_project
        os.environ["WANDB_WATCH"] = "gradients"
        os.environ["WANDB_LOG_MODEL"] = "checkpoint"
    
    if resume_from_checkpoint:
        # Check the available weights and load them
        checkpoint_name = os.path.join(resume_from_checkpoint, "pytorch_model.bin")  # Full checkpoint
        if not os.path.exists(checkpoint_name):
            checkpoint_name = os.path.join(
                resume_from_checkpoint, "adapter_model.bin"
            )  # only LoRA model - LoRA config above has to fit
            resume_from_checkpoint = False  # So the trainer won't try loading its state
        # The two files above have a different name depending on how they were saved, but are actually the same.
        if os.path.exists(checkpoint_name):
            print(f"Restarting from {checkpoint_name}")
            adapters_weights = torch.load(checkpoint_name)
            set_peft_model_state_dict(model, adapters_weights)
        else:
            print(f"Checkpoint {checkpoint_name} not found")
        
    model.print_trainable_parameters()

    if torch.cuda.device_count() > 1:
        # keeps Trainer from trying its own DataParallelism when more than 1 gpu is available
        model.is_parallelizable = True
        model.model_parallel = True
    

    trainer = transformers.Trainer(
        model=model,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_val_dataset,
        callbacks=[CheckpointCallback(stub.results_volume)], # Callback function for committing a checkpoint to Volume when reached
        args=transformers.TrainingArguments(
            output_dir=f"/results/{run_id}",  # Must also set this to write into results Volume's mount location
            warmup_steps=5,
            per_device_train_batch_size=8,
            gradient_accumulation_steps=4,
            max_steps=1000,  # Feel free to tweak to correct for under/overfitting
            learning_rate=2e-5, # ~10x smaller than Mistral's learning rate
            bf16=True,
            optim="adamw_8bit",
            save_strategy="steps",       # Save the model checkpoint every logging step
            save_steps=50,                # Save checkpoints every 50 steps
            evaluation_strategy="steps", # Evaluate the model every logging step
            eval_steps=50,               # Evaluate and save checkpoints every 50 steps
            do_eval=True,                # Perform evaluation at the end of training
            report_to="wandb" if wandb_project else "",         
            run_name=run_id if wandb_project else ""     
        ),
        data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    model.config.use_cache = False  # Silence the warnings. Re-enable for inference!
    trainer.train()  # Run training
    
    model.save_pretrained(f"/results/{run_id}") 
    stub.results_volume.commit()

@stub.local_entrypoint()
def main(run_id: str = "", resume_from_checkpoint: str = None):
    print("Load data to modal volume")
    #load_dataset.remote()
    print("finished load data")

    if not run_id:
        run_id = f"mistral7b-finetune-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    
    print(f"Starting training run {run_id=}.")
    finetune.remote(model_name=BASE_MODEL, run_id=run_id, wandb_project=WANDB_PROJECT, resume_from_checkpoint=resume_from_checkpoint)
    print(f"Completed training run {run_id=}")
    




        






