# Using the OpenRouter API directly

import json
import requests
from rich import print
from my_secrets import MySecrets

secrets = MySecrets()

response = requests.post(
    url=f"{secrets.openrouter_base_url}/chat/completions",
    headers={
        "Authorization": f"Bearer {secrets.openrouter_api_key}",
    },
    data=json.dumps(
        {
            "model": secrets.openrouter_model,
            "messages": [
                {"role": "user", "content": "What is the capital of France?"},
            ],
        }
    ),
)

if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print(f"[bold green]Reply from model:[/bold green] {reply}")

else:
    print(f"[bold red]Error:[/bold red] {response.status_code} - {response.text}")