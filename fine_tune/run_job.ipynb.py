# 1. Connect to your Azure ML workspace
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import CommandJob, Input, CodeConfiguration

# Replace with your workspace details
subscription_id = "<YOUR_SUBSCRIPTION_ID>"
resource_group = "<YOUR_RESOURCE_GROUP>"
workspace = "<YOUR_AML_WORKSPACE_NAME>"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# 2. Configure the training data asset
training_data = Input(
    type="uri_file",
    path="azureml:my_training_data:1"
)

# 3. Reference your GPU compute cluster name
gpu_compute_name = "gpu-cluster-finetune"

# 4. Define the environment for the job
# Option A: Reference a curated GPU environment
env_name = "AzureML-acpt-pytorch-2.2-cuda12.1@latest"

# Option B: Uncomment and use the code below to build a custom environment if needed
# from azure.ai.ml.entities import Environment
# custom_env = Environment(
#     image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest", # Use a CUDA-enabled base image
#     conda_file="./environments/conda_env.yml",
#     name="llm-finetune-env"
# )
# ml_client.environments.create_or_update(custom_env)
# env_name = "llm-finetune-env@latest"


# 5. Build and submit the command job
job = CommandJob(
    display_name="llm-fine-tuning-job",
    code=CodeConfiguration(
        code="./src",
        scoring_script="finetune.py",
    ),
    command="python finetune.py --training_data ${{inputs.training_data}} --epochs 5 --model_name 'meta-llama/Llama-2-7b-hf'",
    inputs={
        "training_data": training_data,
    },
    compute=gpu_compute_name,
    environment=env_name,
    experiment_name="llm-fine-tuning-project",
)

# Example input reference (e.g., datastore path or file dataset)
training_data = Input(
    type="uri_file",
    path="azureml://datastores/workspaceblobstore/paths/data/train.jsonl"
)

# Define command job
job = command(
    display_name="llm-fine-tuning-job",
    description="Fine-tune Llama 2 model on custom dataset",
    experiment_name="llm-fine-tuning-project",
    code="./src",  # 👈 same as CodeConfiguration.code
    command=(
        "python finetune.py "
        "--training_data ${{inputs.training_data}} "
        "--epochs 5 "
        "--model_name 'meta-llama/Llama-2-7b-hf'"
    ),
    inputs={
        "training_data": training_data,
    },
    environment=env_name,
    compute=gpu_compute_name,
)

# Submit job
returned_job = ml_client.jobs.create_or_update(job)
print(f"✅ Job submitted: {returned_job.name}")



# 6. Submit the job and stream the output
returned_job = ml_client.jobs.create_or_update(job)
ml_client.jobs.stream(returned_job.name)

# 7. Get the final job status
print(f"Job Status: {ml_client.jobs.get(name=returned_job.name).status}")
