import os
import json
from openai import AzureOpenAI

class FactualityEvaluator:
    def __init__(self, model_config):
        current_dir = os.path.dirname(__file__)
        prompty_path = os.path.join(current_dir, "factuality.prompty")
        
        # Read the prompty file to get the prompt template
        with open(prompty_path, 'r') as f:
            self.prompt_template = f.read()
        
        # Initialize the OpenAI client based on model_config
        self.client = AzureOpenAI(
            api_key=model_config.get("api_key"),
            api_version=model_config.get("api_version"),
            azure_endpoint=model_config.get("azure_endpoint")
        )
        
        self.model = model_config.get("azure_deployment")

    def __call__(self, *, response: str, **kwargs):
        # Replace placeholders in the prompt template
        prompt = self.prompt_template.replace("{{response}}", response)
        
        llm_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        content = llm_response.choices[0].message.content
        
        try:
            response = json.loads(content)
        except Exception as ex:
            response = content
        
        return response
