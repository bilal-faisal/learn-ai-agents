# Global Config
# Global Default Setup

from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled

secrets =  MySecrets()

external_client = AsyncOpenAI(
    api_key=secrets.gemini_api_key,
    base_url=secrets.gemini_base_url, 
)

set_default_openai_client(external_client)
set_default_openai_api('chat_completions')
set_tracing_disabled(True)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=secrets.gemini_model_name,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is the capital of France?",
)

print(result.final_output)