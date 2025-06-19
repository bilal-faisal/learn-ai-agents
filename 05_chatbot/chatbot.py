import os
import json
import chainlit as cl
from rich import print
from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import set_tracing_disabled
from typing import cast


@cl.on_chat_start
async def on_chat_start():
    print("[bold green]New chat session has started![/bold green]")

    # Load secrets
    secrets = MySecrets()

    # Initialize the OpenAI client with Gemini API details
    external_client = AsyncOpenAI(
        api_key=secrets.gemini_api_key,
        base_url=secrets.gemini_base_url,
    )

    # Disable tracing
    set_tracing_disabled(True)

    # Create an OpenAIChatCompletionsModel instance with the Gemini model
    model = OpenAIChatCompletionsModel(
        model=secrets.gemini_model_name,
        openai_client=external_client,
    )

    # Initialize the agent with the model and instructions
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model,
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])


@cl.on_chat_end
async def on_chat_end():
    print("[bold red]User chat session ended![/bold red]")

    new_chat_history = cl.user_session.get("chat_history", []) or []

    # Load existing chat history if file exists
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            all_chats = json.load(f)
    else:
        all_chats = []

    # Append the new chat session
    all_chats.append(new_chat_history)

    # Write back the updated list
    with open("chat_history.json", "w") as f:
        json.dump(all_chats, f, indent=2)


@cl.on_message
async def on_message(message: cl.Message):
    response = cl.Message(content="Thinking...")
    await response.send()

    chat_history = cl.user_session.get("chat_history", []) or []
    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    chat_history.append(
        {
            "role": "user",
            "content": message.content,
        }
    )

    result = Runner.run_sync(
        starting_agent=agent,
        input=chat_history,
    )

    agent_response = result.final_output

    chat_history.append(
        {
            "role": "assistant",
            "content": agent_response,
        }
    )

    response.content = agent_response
    await response.update()

    cl.user_session.set("chat_history", chat_history)


@cl.set_chat_profiles  # type: ignore
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Gemini",
            icon="/public/gemini.png",
            markdown_description="Supports code generation, creative writing, and research-based answers.",
            starters=[
                cl.Starter(
                    label="Share Something",
                    message="I want to talk about something I really like.",
                    icon="/public/favorite.svg",
                ),
                cl.Starter(
                    label="Brainstorm a New Idea",
                    message="Help me brainstorm a creative idea.",
                    icon="/public/idea.svg",
                ),
            ],
        ),
    ]
