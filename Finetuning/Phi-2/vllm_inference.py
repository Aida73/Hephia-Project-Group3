import os

from modal import Image, Secret, Stub, method, web_endpoint

from transformers import AutoTokenizer

from pydantic import BaseModel
import json

MODEL_DIR = "/model"
BASE_MODEL = "aissatoubalde/lab"


def download_model_to_folder():
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache

    os.makedirs(MODEL_DIR, exist_ok=True)

    snapshot_download(
        BASE_MODEL,
        local_dir=MODEL_DIR,
        token=os.environ["HF_TOKEN"],
    )
    #move_cache()
    
    
image = (
    Image.from_registry(
        "nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.10"
    ) #Add config 
    .pip_install(
        "vllm==0.3.0",
        "huggingface_hub==0.19.4",
        "hf-transfer==0.1.4",
        "torch==2.1.2",
        "transformers",
        "einops",
        "datasets",
        "peft",
        "bitsandbytes",
    )
    # Use the barebones hf-transfer package for maximum download speeds. No progress bar, but expect 700MB/s.
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        download_model_to_folder,
        secrets=[Secret.from_name("my-huggingface-secret-2")],
        timeout=60 * 20,
    )
)

stub = Stub("example-vllm-inference", image=image)


@stub.cls(gpu="H100", secrets=[Secret.from_name("my-huggingface-secret-2")])
class Model:
    def __enter__(self):
        from vllm import LLM

        # Load the model. Tip: MPT models may require `trust_remote_code=true`.
        self.llm = LLM(MODEL_DIR, trust_remote_code=True)
        self.template = """{user}"""

    @method()
    def generate(self, user_question):
        from vllm import SamplingParams

        prompts = self.template.format(system="", user=user_question) 
        sampling_params = SamplingParams(
            temperature=0.75,
            top_p=1,
            max_tokens=200,
            presence_penalty=1.15,
        )
        outputs = self.llm.generate(prompts, sampling_params)
        for output in outputs:
            generated_text = output.outputs[0].text
            print(f"Generated text: {generated_text!r}")
        print(generated_text)
        return generated_text


class Question(BaseModel):
    question: str


@stub.function()
@web_endpoint(method="POST")
def main(user_question:Question):
    model = Model()
    #questions = "What is diabetis?"
    output = model.generate.remote(user_question.question)
    return {"response":output}
