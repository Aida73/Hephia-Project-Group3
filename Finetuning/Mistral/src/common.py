from modal import Stub, Image, Volume, Secret
import os

APP_NAME = "heph3-mistral7b-finetune"

# Latest image hash of winglian/axolotl:main-py3.10-cu118-2.0.1 (2023-12-11)
AXOLOTL_REGISTRY_SHA = (
    "5c19a5154fd522225953b9c3f6206750f4191e0e92ee424f02963f7963ada698"
)
# Need to patch transformers to an older version to avoid checkpointing errors.
TRANSFORMERS_SHA = "5324bf9c07c318015eccc5fba370a81368a8df28"

axolotl_image = (
    Image.from_registry(f"winglian/axolotl@sha256:{AXOLOTL_REGISTRY_SHA}")
    .run_commands(
        "git clone https://github.com/OpenAccess-AI-Collective/axolotl /root/axolotl",
        "cd /root/axolotl && git checkout a581e9f8f66e14c22ec914ee792dd4fe073e62f6",
    )
    .pip_install("huggingface_hub==0.19.4", "hf-transfer==0.1.4")
    .pip_install(
        f"transformers @ git+https://github.com/huggingface/transformers.git@{TRANSFORMERS_SHA}",
        "--force-reinstall",
    )
    .env(dict(HUGGINGFACE_HUB_CACHE="/pretrained", HF_HUB_ENABLE_HF_TRANSFER="1"))
)

vllm_image = (
    Image.from_registry("nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.10")
    .pip_install("vllm==0.2.5")
)

stub = Stub(APP_NAME, secrets=[Secret.from_name("my-wandb-secret-2")])

# Volumes for pre-trained models and training runs.
pretrained_volume = Volume.persisted("heph3-traing-data-vol")
runs_volume = Volume.persisted("heph3-traing-runs-vol")
VOLUME_CONFIG: dict[str | os.PathLike, Volume] = {
    "/pretrained": pretrained_volume,
    "/runs": runs_volume
}
# The following values were not passed to `accelerate launch` and had defaults used instead:
#         `--num_processes` was set to a value of `0`
#         `--num_machines` was set to a value of `1`
#         `--mixed_precision` was set to a value of `'no'`
#         `--dynamo_backend` was set to a value of `'no'