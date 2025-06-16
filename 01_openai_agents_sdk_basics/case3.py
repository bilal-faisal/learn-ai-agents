# Runner Config
# Providing model at runtime

from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.run import RunConfig

secrets = MySecrets()

external_client = AsyncOpenAI(
    api_key=secrets.gemini_api_key,
    base_url=secrets.gemini_base_url,
)

model = OpenAIChatCompletionsModel(
    model=secrets.gemini_model_name,
    openai_client=external_client,
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is the capital of France?",
    run_config=RunConfig(
        model=model,
        tracing_disabled=True,
    )
)

print(result.final_output)