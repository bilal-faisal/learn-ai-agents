import chainlit as cl
from rich import print


@cl.on_chat_start
async def on_chat_start():
    print("[bold green]===============================[/bold green]")
    print("[bold green]A new chat session has started![/bold green]")
    print("[bold green]===============================[/bold green]")


@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=(f'You said: "{message.content}"\n')).send()


@cl.on_chat_end
async def on_chat_end():
    print("[bold red]========================[/bold red]")
    print("[bold red]User chat session ended![/bold red]")
    print("[bold red]========================[/bold red]")


@cl.set_starters  # type: ignore
async def set_starters():
    return [
        cl.Starter(
            label="Check Weather",
            message="I want to ask you about weather.",
            icon="/public/weather.svg",
        ),
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
    ]
