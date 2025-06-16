# Using the OpenAI SDK

from rich import print
from openai import OpenAI
from my_secrets import MySecrets

secrets = MySecrets()

client = OpenAI(
    api_key=secrets.openrouter_api_key,
    base_url=secrets.openrouter_base_url,
)

completion = client.chat.completions.create(
    model=secrets.openrouter_model,
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

reply = completion.choices[0].message.content

print(f"[bold green]Reply from model:[/bold green] {reply}")