# Agent Config
# Agent specific model setup

from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import set_tracing_disabled

secrets = MySecrets()

external_client = AsyncOpenAI(
    api_key=secrets.gemini_api_key,
    base_url=secrets.gemini_base_url,
)

set_tracing_disabled(True)

model = OpenAIChatCompletionsModel(
    model=secrets.gemini_model_name,
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

print(result.final_output)