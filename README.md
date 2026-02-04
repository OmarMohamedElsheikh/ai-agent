## A terminal-based AI chatbot built on the Gemini API that supports automatic function calling, verbose token inspection, and extensible tool execution.

Designed as a learning-focused agent framework, not just a chat interface

## Features

- Conversational AI using the Gemini API.
- Function calling capabilities.
- Verbose output for debugging and insights into token usage.


## Technical Description

The Gemini AI Chatbot Agent leverages the powerful Gemini API for natural language understanding and generation.
It's designed with a robust function-calling mechanism that allows the AI to interact with external tools and services.
When a user prompt is received, the agent analyzes the input and, if necessary, identifies and executes relevant predefined functions. 
This architecture enables the chatbot to perform dynamic actions beyond simple conversational responses, such as performing calculations, retrieving information, or interacting with other systems. 
The system also includes verbose logging to provide insights into the AI's decision-making process, including token usage and the results of function calls.


### Architecture

The project is structured with the following key components:

*   **`main.py`**: The core of the application. It handles:
    *   Loading environment variables (API keys).
    *   Parsing command-line arguments (e.g., `--verbose` for detailed output).
    *   Initializing the Gemini client.
    *   Managing the conversational flow, including sending messages to the Gemini API and processing its responses.
    *   Calling external functions based on the model's function call predictions.
    *   Handling API rate limits and errors.
*   **`config.py`**: This file is likely used for storing configuration settings, although its current content is minimal. It could be expanded to include model parameters, API endpoints, or other customizable settings.
*   **`prompts.py`**: Contains the `system_prompt` which guides the AI's behavior and personality. This is crucial for defining the chatbot's role and how it should interact with users.
*   **`call_function.py`**: This file acts as an intermediary for function calls. It defines `available_functions` (a collection of tools the AI can use) and the `call_function` logic, which executes the appropriate function based on the AI's request.
*   **`functions/`**: This directory (not explicitly detailed in the provided content, but implied by `call_function.py`) would contain individual Python modules or scripts that define the actual functions the AI can call (e.g., a calculator, a file system utility, etc.).
*   **`.env`**: Stores environment-specific variables like the `GIMINI_API_KEY`, keeping sensitive information out of the codebase.
*   **`README.md`**: Provides an overview of the project, setup instructions, and usage details.

### How it Works

1.  **Initialization**: When `main.py` starts, it loads the Gemini API key from the `.env` file and sets up the Gemini client.
2.  **User Interaction**: The chatbot enters a loop, prompting the user for input. Each user message is added to the conversation history.
3.  **AI Processing**: The conversation history, along with the `system_prompt` and `available_functions`, is sent to the Gemini API.
4.  **Function Calling (if applicable)**:
    *   If the Gemini model determines that a function needs to be called to fulfill the user's request, it will return a `function_call` object.
    *   `call_function.py` receives this object and executes the corresponding function from the `functions/` directory.
    *   The result of the function call is then sent back to the Gemini API as part of the conversation history, allowing the AI to generate a more informed response.
5.  **AI Response**: If no function call is needed, or after a function call has been processed, the Gemini model generates a textual response, which is then displayed to the user.
6.  **Conversation Continuation**: The loop continues, allowing for multi-turn conversations until the user decides to exit.

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
    pip install google-generativeai python-dotenv
    ```

4.  **Set up your Gemini API Key:**

    Obtain a Gemini API key from the [Google AI Studio](https://aistudio.google.com/).
    Create a `.env` file in the root directory of the project and add your API key:

    ```env
    GIMINI_API_KEY="YOUR_API_KEY"
    ```

## Usage
### Run the Chatbot

Start the chatbot with:
```bash
python main.py
```

You’ll see a prompt like:

```
You:
```

Type your message and press Enter to chat with the agent.

Enable verbose mode to see token usage and function call outputs:

```bash
python main.py --verbose
```

**Verbose mode prints:**
- Prompt token count
- Response token count
- Function call responses (if any)

The chatbot maintains conversation history across turns. The model may call predefined functions automatically when needed. Each response is generated with a maximum of 20 internal iterations to avoid infinite loops. After each exchange, you’ll be asked whether you want to continue:

```
Do you want to continue (y/n)?
```

Any input other than y exits the program. When you choose to stop the conversation, the program exits cleanly:

```
exiting chat.
```


### Arguments

*   `--verbose` (optional): Enable verbose output to display prompt tokens, response tokens, and function call results.

## Why This Project Exists

This project was built to explore:
- Gemini’s function-calling mechanism in practice
- Tool execution loops in conversational agents
- Debuggable agent behavior via token-level verbosity

It is intentionally simple, terminal-based, and extensible.


## Example Interaction

User:
> calculate 12 * 8

Agent:
> The result is 96.

[Function called: calculator.multiply]


## Limitations

- Single-user
- No persistent memory beyond runtime
- Limited built-in tools

## Possible Extensions

- Persistent memory store
- More complex tool schemas
