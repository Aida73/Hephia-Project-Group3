from modal import method, gpu
from typing import Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shared import stub, MODEL_DIR, VOLUME_CONFIG
GPU_CONFIG = gpu.A100(memory=80, count=2)


@stub.cls(gpu=GPU_CONFIG, volumes=VOLUME_CONFIG)
class Model():
    def __init__(self, run_id: Optional[str] = None):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import PeftModel
    
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_DIR,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )

        if run_id:
            self.model = PeftModel.from_pretrained(  # model with adapter
                base_model,
                f"/results/{run_id}",
                torch_dtype=torch.bfloat16,
            )
        else:
            self.model = base_model
        
        self.eval_tokenizer = AutoTokenizer.from_pretrained(
            MODEL_DIR,
            add_bos_token=True,
            trust_remote_code=True,
            padding_side="right",
        )

        self.template = "[INST] <<SYS>>\nUse the Input to provide an answer of a medical question.\n<</SYS>>\n\nInput:\n{question} [/INST]\n\Response:"
    
    def tokenize_prompt(self, prompt: str = ""):
        return self.eval_tokenizer(prompt, return_tensors="pt").to("cuda")
    
    @method()
    async def generate(self, question: str):
        import torch

        model_input = self.tokenize_prompt(self.template.format(question=question))
        self.model.eval()
        with torch.no_grad():
            print(
                self.eval_tokenizer.decode(
                    self.model.generate(**model_input,max_new_tokens=200,eos_token_id=self.eval_tokenizer.eos_token_id,
                    )[0],skip_special_tokens=True,
                )
            )


@stub.local_entrypoint()
def main(run_id: str):
    question = "What is Diabet?"
    print("=" * 20 + "Generating without adapter" + "=" * 20)
    for response in Model().generate.map(question):
        print(response)



    
    


