# Using the OpenAI Agents SDK

from rich import print
from openai import AsyncOpenAI
from my_secrets import MySecrets
from agents import set_tracing_disabled
from agents import Agent, Runner, OpenAIChatCompletionsModel

secrets = MySecrets()

external_client = AsyncOpenAI(
    api_key=secrets.openrouter_api_key,
    base_url=secrets.openrouter_base_url,
)

set_tracing_disabled(True)

model = OpenAIChatCompletionsModel(
    model=secrets.openrouter_model,
    openai_client=external_client,
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is the capital of France?",
)

print(f"[bold green]Reply from model:[/bold green] {result.final_output}")