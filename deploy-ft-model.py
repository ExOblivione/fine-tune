import json
import requests

token = ""
resource_group = ""
resource_name = ""
subscription = ""
finetuned_model = "gpt-4.1-nano-2025-04-14.ft-0eb9b13bbfac456c8c0fbe1847ad6d06"

# deploy the fine-tuned model
deploy_params = {'api-version': "2025-07-01-preview"} 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "developertier", "capacity": 50},
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": finetuned_model,
        }
    }
}
deploy_data = json.dumps(deploy_data)

request_url = f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}/deployments/{finetuned_model}'

print('Creating a new deployment...')

r = requests.put(request_url, params=deploy_params, headers=deploy_headers, data=deploy_data)

print(r)
print(r.reason)
print(r.json())
