import chainlit as cl
from rich import print


@cl.on_chat_start
async def on_chat_start():
    print("[bold green]===============================[/bold green]")
    print("[bold green]A new chat session has started![/bold green]")
    print("[bold green]===============================[/bold green]")


@cl.on_chat_end
async def on_chat_end():
    print("[bold red]========================[/bold red]")
    print("[bold red]User chat session ended![/bold red]")
    print("[bold red]========================[/bold red]")


@cl.on_message
async def on_message(message: cl.Message):
    selected_profile = cl.user_session.get("chat_profile")

    await cl.Message(
        content=(
            f'You said: "{message.content}"\n\n'
            f"This message was sent to the **{selected_profile}** profile."
        )
    ).send()


# In case you want general starters for the chat
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


@cl.set_chat_profiles  # type: ignore
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Gemini",
            icon="/public/gemini.png",
            markdown_description="Supports code generation, creative writing, and research-based answers.",
            # In case you want to set specific starters for this profile, you can do so here
            starters=[
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
            ],
        ),
        cl.ChatProfile(
            name="OpenAI",
            icon="/public/openai.png",
            markdown_description="Ideal for deep thinking, creativity, and accurate answers.",
            # Here we have not set any specific starters, so the general starters will be used
        ),
    ]
