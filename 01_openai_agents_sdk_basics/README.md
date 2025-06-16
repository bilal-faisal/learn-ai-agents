# 🤖 OpenAI Agents SDK — Basics

Welcome to the basics of the OpenAI Agents SDK. This module demonstrates three different ways to set up and run OpenAI-compatible agents using the SDK — from simple global clients to flexible runtime model injection.

## 📁 Project Structure

```
agents_basics/
├── case1.py           # Global default client configuration
├── case2.py           # Agent-specific model setup
├── case3.py           # Dynamic model injection via RunConfig
├── my_secrets.py      # Loads and validates required environment variables
├── main.py            # CLI-friendly summary (optional)
├── .env.example       # Template for your environment variables
└── myproject.toml     # Project dependencies (used by uv)
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/bilal-faisal/openai-agents-sdk.git
cd openai-agents-sdk/01_agents_basics
```

### 2. Set Up the Environment with uv

```bash
uv venv
uv sync
```

### 3. Create Your .env File

```bash
cp .env.example .env
```

Then fill in your `.env` file like this:

```env
GEMINI_API_KEY=your-api-key
GEMINI_BASE_URL=https://your-base-url
GEMINI_MODEL_NAME=gpt-4.1
```

## 🧪 Run Examples

Each case demonstrates a different configuration strategy. You can run them like so:

```bash
python case1.py   # Global default client setup
python case2.py   # Agent-specific model setup
python case3.py   # Runtime-configured model via RunConfig
```

## 📦 Dependencies

This project uses:

- `openai-agents-sdk`
- `rich`
- `python-dotenv`

All dependencies are managed with `uv` and defined in `myproject.toml`.

## 🧠 About my_secrets.py

This file handles all environment variable validation on startup. It ensures that:

- `GEMINI_API_KEY`
- `GEMINI_BASE_URL`
- `GEMINI_MODEL_NAME`

...are set before any agent runs.