from openai import AzureOpenAI
from evaluators import build_evaluation_summary, get_evals

endpoint = ""
model_name = "gpt-4.1-nano"
deployment = "gpt-4.1-nano"

subscription_key = ""
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Upload the training file
print("Uploading training file...")
with open("data.jsonl", "rb") as f:
    training_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

print(f"Training file uploaded. File ID: {training_file.id}")

# Start fine-tuning codes here :)
job = client.fine_tuning.jobs.create(
    model=model_name,
    training_file=training_file.id,
    hyperparameters={
        "n_epochs": 3
    }
)

print("Fine-tuning job created. Job ID:", job.id)

# Retrieve specific job
job = client.fine_tuning.jobs.retrieve(job.id)
print("Status:", job.status)
print("Fine-tuned model:", job.fine_tuned_model)
