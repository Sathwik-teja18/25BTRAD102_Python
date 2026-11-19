# GENESIS v4.0 — self-evolving local AI agent

A clean-slate Python starter that uses Ollama locally. The stable kernel creates a mutable `cortex.py`, can generate separate skill plugins, stores persistent notes in `memory.json`, and keeps code backups.

## What's included

- **Immutable kernel** in `genesis.py`: Ollama API client, model-tier selection, terminal approval gate, code validation, backups, hot-loading, skill loading, and recovery.
- **Mutable cortex**: generated on first launch. This is the module GENESIS can rewrite.
- **Separate skills**: generated into `skills/` by `/skill ...`.
- **Persistent memory**: `memory.json` stores notes and evolution/skill history.
- **Model profiles**: general `qwen3.5:4b`, coding `qwen2.5-coder:3b`, reasoning `deepseek-r1:7b`. If a profile model is missing, GENESIS asks before downloading it.
- **Online chat (optional)**: OpenAI-first for ordinary non-coding chat, with local Ollama fallback and a persisted daily USD budget. OpenAI must be explicitly configured; code-generation requests remain local.
- **Terminal access**: `shell: <command>` and model-requested terminal commands both display the command and require interactive approval before running.

The three profile tags are currently listed in the Ollama model library: [Qwen3.5](https://registry.ollama.com/library/qwen3.5), [Qwen2.5-Coder](https://registry.ollama.com/library/qwen2.5-coder), and [DeepSeek-R1](https://registry.ollama.com/library/deepseek-r1). Model size, available tags, speed, and hardware requirements can change, so inspect the profile configuration before letting the agent download models.

## Requirements

- Python 3.11+ (the code uses only the Python standard library)
- Ollama installed and running locally
- Internet access for first-time model pulls

No `pip install requests` is required; the kernel and OpenAI provider use Python's built-in HTTP libraries.

## Windows quick start

1. Create a fresh folder, for example `C:\\GENESIS`.
2. Save `genesis.py` there.
3. Open PowerShell in that folder.
4. Start Ollama, then run:

   ```powershell
   py -3.11 .\genesis.py
   ```

5. On the first request, GENESIS asks before downloading a missing profile model. A pull can take several GB and some time; declining it makes GENESIS try an already-installed model.

## Optional OpenAI-first chat

Ordinary non-coding chat uses OpenAI first when configured, then falls back to local Ollama if configuration, connectivity, or the daily budget prevents an online response. Requests related to coding, skills, or evolution stay on Ollama. Online chat sends the current user message and a generic system instruction; saved memory is not sent. Do not send secrets or other content you do not want processed by OpenAI.

Configure these as **user environment variables in Windows Settings**, then restart the terminal. Do not put an API key in source code, a checked-in file, or a command that will be saved in shell history.

| Variable | Required | Meaning |
|---|---:|---|
| `GENESIS_OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `GENESIS_OPENAI_MODEL` | Yes | Model name available to your API account |
| `GENESIS_OPENAI_INPUT_USD_PER_1M` | Yes | Current input price in USD per million tokens |
| `GENESIS_OPENAI_OUTPUT_USD_PER_1M` | Yes | Current output price in USD per million tokens |
| `GENESIS_DAILY_BUDGET_USD` | No | Daily limit; defaults to `1.00` USD, reset by UTC date |

Set the input and output prices using the current pricing for your selected model. If the key, model, or prices are missing or invalid, GENESIS makes no OpenAI request and uses Ollama instead. The local `usage.json` ledger records estimated charges using those configured prices and reserves budget before each request; requests with uncertain billing keep their reservation until the next UTC day. Changing model, prices, or budget during a UTC day disables further online calls until the next day, preventing mixed-rate accounting.

This is a **client-side guard, not a guaranteed hard spending limit**: the ledger can be edited or deleted, separate copies of GENESIS have separate ledgers, and actual provider billing can differ because of price changes, taxes, or billing rules. Set an account-side spending limit with OpenAI as well, and check both the local ledger and provider usage.

## Useful first commands

```text
/help
/models
remember I prefer concise technical explanations
memory
/evolve Add a 'stats' command for CPU usage, RAM usage, and battery percentage using psutil, with a clear message if psutil is not installed.
/skill Add a calculator skill for basic arithmetic expressions. Do not use eval.
shell: py -3.11 -m pip install psutil
/rollback
/code
```

The terminal install example will ask for approval before executing. For calculator plugins, do not approve code that uses `eval` or dynamically executes source.

## Model tiers

| Tier | Default model | Purpose |
|---|---|---|
| `general` | `qwen3.5:4b` | ordinary questions and chat |
| `coding` | `qwen2.5-coder:3b` | rewrites, skills, debugging |
| `reasoning` | `deepseek-r1:7b` | harder analysis and multi-step reasoning |

Change `MODEL_PROFILES` in `genesis.py` to suit your hardware and preferences. The agent caps the Ollama context window at 4096 to reduce memory pressure. If one model returns an Ollama error, it tries other installed chat models before failing.

## Important safety notes

- A model-generated Python module runs inside the same Python process. AST checks and a review prompt catch some mistakes, but **they are not a true security sandbox**. Review the diff before approving it and run this project in a dedicated folder; do not run it as Administrator.
- Terminal commands always require a confirmation prompt. Never approve a command you don't understand.
- Missing profile models and custom models are downloaded only after you confirm the prompt.
- Keep backups. `/rollback` restores `cortex_backups/latest.bak`; `/reset` re-seeds `cortex.py` but preserves memory and skills.
- Run only plugins you trust. A plugin can have side effects at import or execution time, so review it before approval.

## Troubleshooting Ollama HTTP 500

1. Run `ollama list` in another terminal and verify the model is installed.
2. Confirm the Ollama service is running and available at `http://127.0.0.1:11434`.
3. Try a smaller profile model, reduce `MAX_CONTEXT`, or select another installed model with `/model <tag>`.
4. Read the exact error printed by the kernel. HTTP 500 can be caused by memory pressure, model loading failure, an unsupported model, or another Ollama runtime error; it is not always a context-window problem.

## Tests

Run the offline kernel and provider tests from this directory:

```powershell
python -m unittest -v test_genesis.py test_openai_provider.py
```
