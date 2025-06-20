import os
import json
import chainlit as cl
from rich import print
from my_secrets import MySecrets
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import function_tool, set_tracing_disabled
from typing import cast
from openai.types.responses import ResponseTextDeltaEvent


@function_tool
@cl.step(type="fetch_weather")  # type: ignore
async def fetch_weather(location: str) -> str:
    """Fetch the weather for a given city.

    Args:
        location: The city name to fetch the weather for.
    """
    return f"The current weather in {location} is sunny with a temperature of 25°C."


@function_tool
@cl.step(type="student_finder")  # type: ignore
def student_finder(roll_number: int) -> str:
    """Find a student by roll number.

    Args:
        roll_number: The roll number of the student to find.
    """
    data = {
        1: {"name": "Ahmed Khan", "age": 20, "grade": "A", "major": "Computer Science"},
        2: {"name": "Fatima Ali", "age": 22, "grade": "B", "major": "Mathematics"},
        3: {"name": "Sara Ahmed", "age": 21, "grade": "A", "major": "Physics"},
        4: {"name": "Ali Raza", "age": 23, "grade": "C", "major": "Chemistry"},
        5: {"name": "Zainab Shah", "age": 19, "grade": "B", "major": "Biology"},
    }
    student: dict | str = data.get(roll_number, "Student not found.")

    if isinstance(student, str):
        return student

    return (
        f"Student found: Name: {student['name']}, Age: {student['age']}, "
        f"Grade: {student['grade']}, Major: {student['major']}"
    )


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
        instructions=f"""You are a helpful assistant. When the user requests multiple actions 
        (e.g., finding a student and checking the weather), handle each one separately. 
        Call only one tool at a time, then return the result before continuing.""",
        model=model,
        tools=[fetch_weather, student_finder],
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])


@cl.on_chat_end
async def on_chat_end():
    print("[bold red]User chat session ended![/bold red]")

    new_chat_history = cl.user_session.get("chat_history", []) or []

    # Load existing chat history if file exists
    if os.path.exists("chat_history_f2.json"):
        with open("chat_history_f2.json", "r") as f:
            all_chats = json.load(f)
    else:
        all_chats = []

    # Append the new chat session
    all_chats.append(new_chat_history)

    # Write back the updated list
    with open("chat_history_f2.json", "w") as f:
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
            markdown_description="I am a chatbot, capable of fetching weather & student details through function tools.",
            starters=[
                cl.Starter(
                    label="Fetch Weather",
                    message="I want to get the current weather for a specific city.",
                    icon="/public/weather.svg",
                ),
                cl.Starter(
                    label="Find Student",
                    message="I want to find a student by their roll number.",
                    icon="/public/student.svg",
                ),
            ],
        ),
    ]
