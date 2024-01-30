import os
from modal import Image, Secret, Stub, Volume
from dotenv import load_dotenv

load_dotenv()

MODEL_DIR = "/model"
BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def download_model_to_folder():
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache

    os.makedirs(MODEL_DIR, exist_ok=True)

    snapshot_download(
        BASE_MODEL,
        local_dir = MODEL_DIR,
        token=os.getenv('HF_TOKEN')
    )
    move_cache()

image = (
    Image.from_registry(
    "nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.10"
    )
    .pip_install("vllm==0.2.5", 
                "huggingface_hub==0.19.4",
                "hf-transfer==0.1.4",
                "bitsandbytes==0.41.1",
                "peft",
                # "transformers",
                # "ctransformers",
                "accelerate==0.24.1",
                "datasets",
                "scipy",
                "wandb"
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "0"})
    .run_function(
        download_model_to_folder,
        secret=Secret.from_name("my-huggingface-secret"),
        timeout=60 * 20, 
    )
    )

stub = Stub("heph-g3-mistral7B-finetuning", image=image)


# Setting up persisting Volumes to store our training data and finetuning results across runs
stub.training_data_volume = Volume.persisted("heph3-traing-data-vol")
stub.results_volume = Volume.persisted("heph3-results-vol")

# Defining mount paths for Volumes within container
VOLUME_CONFIG = {
    "/training_data": stub.training_data_volume,
    "/results": stub.results_volume,
}