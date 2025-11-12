from openai import AzureOpenAI
from evaluators import build_evaluation_summary, get_evals

endpoint = ""
subscription_key = ""
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

finetuned_model = "gpt-4.1-nano-2025-04-14.ft-0eb9b13bbfac456c8c0fbe1847ad6d06"

# Evaluate deployed model
user_message = "What are the compliance requirements for handling personal data?"

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions about compliance and security.",
        },
        {
            "role": "user",
            "content": user_message,
        }
    ],
    max_completion_tokens=300,
    temperature=0.5,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=finetuned_model # changed this only
)

assistant_text = response.choices[0].message.content
print("Assistant output:")
print(assistant_text)
print("Evaluation results:")
print(build_evaluation_summary(get_evals(user_message, assistant_text)))
