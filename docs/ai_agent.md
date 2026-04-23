---
hide:
  - navigation
---

# 🤖 Agentic AI Integration

BfxPM features a built-in **AI Assistant** designed to help bioinformaticians manage their projects, answer technical questions, and automate repetitive tasks. This system is powered by the **SmolAgents** framework and is optimized for both privacy and performance.

---

## 🌟 Overview

The BfxPM AI suite is not just a chat interface; it is a **Project-Aware Agent**. It understands the context of your research, the structure of your files, and the metadata of your project.

### Key Capabilities:
- **Project Context**: The agent can read your `project_tracker.yaml`, directory structure, and basic file contents to provide tailored advice.
- **Tool-Assisted**: It has access to specialized tools for listing files, checking system resources, and reading documentation.
- **Safety-First**: A dedicated **Safety Interceptor** prevents accidental data loss from destructive suggestions.
- **Transparent Reasoning**: Watch the agent's logic in real-time with the "Internal Thoughts" panel.

---

???+ warning "AI Setup Guard"

    - In `bfxpm ai setup`, if you select any cloud provider (Gemini, OpenAI, Anthropic, Groq, or Mistral), the tool now displays a **⚠️ Privacy Alert** panel.
    - It informs the user that prompts and metadata may be processed outside the EU and requires an explicit `yes/no` confirmation to proceed.
    - Selecting **Ollama** remains the recommended path for 100% local, EU-compliant execution.

## ⚙️ Setup

Before you can use the AI agent, you need to configure your environment.

```bash
bfxpm ai setup
```

This command runs an interactive assistant. **Note**: You can type `q`, `exit`, or `abort` at any prompt to cancel the setup process immediately.

The assistant will prompt you to:

1. **Choose a Provider**: Select between:
    - **Ollama (Local)**: Recommended for privacy-first research.
    - **Google Gemini**: Top-tier cloud intelligence via the new GenAI SDK.
    - **OpenAI (ChatGPT)**: Industry-standard models like GPT-4o.
    - **Anthropic (Claude)**: World-class reasoning with Claude 3.5 Sonnet.
    - **Groq**: Llama-3 models at lightning-fast speeds.
    - **Mistral AI**: European-built leading open-weight models.
2. **API Key**: Provide the key for your selected provider. BfxPM stores them securely in an internal dictionary so you can switch providers without re-entering keys.
3. **Model Selection**: Choose your preferred model (e.g., `gpt-4o`, `claude-3-5-sonnet`, `llama-3.1-70b`).

---

## 💬 Interaction Modes

There are two primary ways to interact with the BioAssistant.

### 1. The Interactive Chat (`chat`)
For complex, multi-step tasks or general research support.

```bash
bfxpm ai chat
```

Inside the chat, you can ask things like:

- *"What is the best way to organize my differential expression results?"*
- *"Can you show me the current project structure and suggest improvements?"*
- *"Explain the difference between BAM and CRAM formats."*

### 2. Single Question Mode (`ask`)
For quick answers or single actions without entering a full chat session.

```bash
bfxpm ai ask "How many FASTQ files do I have in my raw data folder?"
```

---

## 🛡️ Safety & Privacy

### The Safety Interceptor
One of the most powerful features of the BfxPM agent is the **Safety Interceptor**. If the agent suggests a command that could be destructive (such as `rm`, `mv`, or `rmdir`):

1. **Automatic Backup**: BfxPM creates a timestamped backup of the target directory in `.bfxpm/backups/`.
2. **Double Confirmation**: The CLI will pause and require a manual `y/n` confirmation from you before executing the command.

### Privacy-First Execution
We understand the sensitivity of genomic research data.

- **Ollama Integration**: By choosing the Ollama provider, you can run the entire AI stack **locally on your own hardware**. Your metadata, prompts, and project details never leave your machine.
- **Encrypted Keys**: Your API keys are stored securely in your local user configuration and are never shared or uploaded.

---

## 📂 Developer's Note: SmolAgents
Under the hood, BfxPM uses a custom _ReAct (Reasoning and Acting)_ loop implementation via `smolagents`. This allows the tool to maintain a minimal memory footprint while providing high-level reasoning capabilities. The BioAssistant is specifically tuned for the **Python 3.13** environment and utilizes the latest `google-genai` SDK for lightning-fast responses.
