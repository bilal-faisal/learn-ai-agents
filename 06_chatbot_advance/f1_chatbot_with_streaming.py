import os
import json
import chainlit as cl
from rich import print
from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import set_tracing_disabled
from typing import cast
from openai.types.responses import ResponseTextDeltaEvent


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
    if os.path.exists("chat_history_f1.json"):
        with open("chat_history_f1.json", "r") as f:
            all_chats = json.load(f)
    else:
        all_chats = []

    # Append the new chat session
    all_chats.append(new_chat_history)

    # Write back the updated list
    with open("chat_history_f1.json", "w") as f:
        json.dump(all_chats, f, indent=2)


@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    chat_history = cl.user_session.get("chat_history", []) or []
    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    chat_history.append(
        {
            "role": "user",
            "content": message.content,
        }
    )

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=chat_history,
        )

        # Streaming the response
        msg.content = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                await msg.stream_token(event.data.delta)

        await msg.update()

        chat_history.append(
            {
                "role": "assistant",
                "content": result.final_output,
            }
        )
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        print(f"[bold red]Error during message processing: {e}[/bold red]")

        msg.content = "An error occurred while processing your message."
        await msg.update()


@cl.set_chat_profiles  # type: ignore
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Gemini",
            icon="/public/gemini.png",
            markdown_description="I am a chatbot, capable of answering in streaming mode.",
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
