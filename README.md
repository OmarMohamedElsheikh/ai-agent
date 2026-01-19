# Gemini AI Chatbot Agent

This project is an AI chatbot agent built with the Gemini API. It can interact with users, understand their prompts, and execute functions based on the conversation.

## Features

- Conversational AI using the Gemini API.
- Function calling capabilities.
- Verbose output for debugging and insights into token usage.

## Setup

To set up the project, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt  # Assuming you have a requirements.txt, or install individual packages like google-generativeai, python-dotenv
    ```

4.  **Set up your Gemini API Key:**

    Obtain a Gemini API key from the [Google AI Studio](https://aistudio.google.com/).
    Create a `.env` file in the root directory of the project and add your API key:

    ```env
    GIMINI_API_KEY="YOUR_API_KEY"
    ```

## Usage

Run the `main.py` script with your desired user prompt:

```bash
python main.py "Your user prompt here"
```

### Arguments

*   `user_prompt` (required): The prompt you want to send to the AI agent.
*   `--verbose` (optional): Enable verbose output to display prompt tokens, response tokens, and function call results.

### Example

```bash
python main.py "What is the capital of France?"
```

```bash
python main.py --verbose "Calculate 10 plus 5"
```
