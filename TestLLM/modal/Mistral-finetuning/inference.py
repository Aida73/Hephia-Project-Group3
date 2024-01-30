import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modal import method, Secret
from shared import stub, MODEL_DIR, VOLUME_CONFIG


@stub.cls(gpu="A100", secret=Secret.from_name("my-huggingface-secret"))
class Model:
    def __enter__(self):
        from vllm import LLM

        self.llm = LLM(MODEL_DIR)
        self.template = """<s>[INST] <<SYS>>
        {system}
        <</SYS>>
        {user} [/INST]"""
    
    @method()
    def generate(self, user_questions):
        from vllm import SamplingParams

        prompts = [
            self.template.format(system="", user=q) for q in user_questions
        ]

        sampling_params = SamplingParams(
            temperature=0.75,
            top_p=1,
            max_tokens=800,
            presence_penalty=1.15,
        )
        result = self.llm.generate(prompts, sampling_params)
        num_tokens = 0
        for output in result:
            num_tokens += len(output.outputs[0].token_ids)
            print(output.prompt, output.outputs[0].text, "\n\n", sep="")
        print(f"Generated {num_tokens} tokens")


@stub.local_entrypoint()
def main():
    model = Model()
    questions = [
        "What is Diabet?",
        "What are Breast Cancer symptoms?",
        "What is caused frequent headache?"  
    ]
    model.generate.remote(questions)