# Basic Stateful Chainlit Application

import chainlit as cl
from rich import print


@cl.on_chat_start
async def on_chat_start():
    print("[bold green]===============================[/bold green]")
    print("[bold green]A new chat session has started![/bold green]")
    print("[bold green]===============================[/bold green]")

    cl.user_session.set("chat_history", [])


@cl.on_message
async def on_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history", []) or []
    chat_history.append(
        {
            "role": "user",
            "content": message.content,
        }
    )

    response = f'You said: "{message.content}"'
    chat_history.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    cl.user_session.set("chat_history", chat_history)

    await cl.Message(content=response).send()

    print("[bold blue]=========================================[/bold blue]")
    print("[bold blue]==========Chat History Updated!==========[/bold blue]")
    print("[bold blue]=========================================[/bold blue]")
    print(chat_history)


@cl.on_chat_end
async def on_chat_end():
    print("[bold red]========================[/bold red]")
    print("[bold red]User chat session ended![/bold red]")
    print("[bold red]========================[/bold red]")
