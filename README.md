# Friday

A local, terminal-based AI agent powered by Google's Gemini API. Friday can search the web, check the current date/time, and read/write files on your behalf — deciding on its own which tools to use based on what you ask, and reasoning across multiple tool calls when a single one isn't enough. Conversations are saved locally, so you can pick up a past chat right where you left off.

Built as a refresher project to rebuild hands-on Python and AI-integration skills after time away from active development.

## Features

- **Multi-tool function calling**: Friday decides which tool(s) a request needs and calls them itself — no manual routing required.
  - `web_search` — live web search via the Tavily API
  - `current_datetime` — resolves relative time expressions ("today", "the latest") that the model can't reliably infer on its own
  - `read_file` / `write_file` — sandboxed local file access, confined to a dedicated `files/` directory
- **Multi-step reasoning loop**: Friday can chain tool calls — e.g. check today's date, then use it to run a time-sensitive search — before producing a final answer, with a safety limit to prevent runaway loops.
- **Sandboxed, confirmation-gated file access**: file paths are sanitized to block path traversal (`../../etc`), and any file write or overwrite requires explicit user confirmation first.
- **Persistent, resumable memory**: every conversation is saved as its own JSON file, complete with an auto-generated title. On startup, pick a past conversation to resume — full history included — or start fresh.
- Crash-safe input handling throughout the CLI (invalid menu choices, non-numeric input, and empty conversation lists are all handled gracefully).

## Requirements

- Python 3.12+
- A [Gemini API key](https://ai.google.dev/)
- A [Tavily API key](https://tavily.com/) (free tier: 1,000 searches/month)

## Installation

1. Clone or download this repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=your_chosen_gemini_model
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

Run the script:

```bash
python3 main.py
```

You'll be prompted to start a new chat, resume a past one, or exit. From there, just talk to Friday — it'll decide on its own when a tool is needed.

### Example Interaction

```
Hello, I'm Friday, your friendly AI assistant!
 Please select an action:
1. Start new chat
2. Continue existing chat
3. Exit
1
○ You:
Who won the latest Wimbledon? Check the date first
➤ Called current_datetime({'current_date': True})
➤ Called web_search({'query': "who won the 2026 Wimbledon men's and women's singles"})
● Friday:
The latest Wimbledon tournament took place in 2026. Here are the winners:

*   **Men's Singles:** Jannik Sinner, who defeated Alexander Zverev.
*   **Women's Singles:** Linda Nosková, who defeated Karolína Muchová.
```

To exit the chat loop, type `q`, `exit`, or `quit`.

## File Structure

- `main.py` — CLI entry point: the startup menu, the conversation picker, and the main chat loop.
- `utils.py` — environment/config loading, and the persistent memory layer (`save_history`, `fetch_history`, `list_conversations`, `print_conversations`, `get_int_input`).
- `tools/` — one module per tool, each exposing both the callable Python function and its Gemini tool declaration:
  - `web_search.py`
  - `current_datetime.py`
  - `read_write_files.py`
- `history/` — one JSON file per conversation (auto-created).
- `files/` — the sandboxed directory `read_file`/`write_file` are confined to (auto-created).

## Code Overview

- **The tool-calling loop (`get_response`)**: sends the user's input to Gemini along with the available tool declarations. If Gemini responds with a function call instead of text, Friday executes the matching function (via a `name → function` dispatch dict) and sends the result back — repeating this as many times as needed until Gemini returns a real answer, or a safety counter (10 rounds) forces a stop.
- **Tool declarations**: each tool is described to Gemini as a JSON schema (name, description, parameters) separate from the Python function itself — this is what lets Gemini decide _when_ and _how_ to call a tool, without ever running your code directly.
- **Memory**: each conversation is identified by a timestamp-based ID and stored as its own JSON file, holding its title, message history, and the Gemini `previous_interaction_id` needed to resume the server-side conversation thread where possible. Conversations are listed newest-first by file modification time.
- **Safety**: file tools sanitize incoming filenames with `os.path.basename()` before touching disk, and prompt for explicit confirmation before any overwrite or append.

## Notes

- Gemini's free tier retains server-side conversation state for only 1 day — Friday's local JSON history is what makes resuming genuinely reliable beyond that window.
- Tool calls are printed to the terminal as they happen (`➤ Called ...`), so you can see exactly what Friday is doing, not just its final answer.
- `files/` and `history/` are created automatically on first run if they don't already exist.

## Future Improvements

- Support for local models (e.g. via Ollama) as an alternative to the Gemini API
- Additional tools — calculator, Wikipedia lookup, currency conversion, translation
- Automated test suite (`pytest`) covering the tool-calling loop, path-traversal protection, and memory persistence
- Containerization with Docker
- CI via GitHub Actions
