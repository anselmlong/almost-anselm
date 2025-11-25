from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./merged-almost-anselm",
    repo_id="anselmlong/almost-anselm-merged",  # You can change the name
    repo_type="model"
)

