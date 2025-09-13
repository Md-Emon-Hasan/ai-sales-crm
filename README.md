# Conversation Management & JSON Schema Extraction (Groq OpenAI-Compatible) - Yardstick
**Author:** Md. Hasan Imon  
**Contact:**
- Email: emon.mlengineer@gmail.com
- WhatsApp: [+8801834363533](https://wa.me/8801834363533)
- GitHub: [Md-Emon-Hasan](https://github.com/Md-Emon-Hasan)
- LinkedIn: [Md Emon Hasan](https://www.linkedin.com/in/md-emon-hasan-695483237/)
- Portfolio: [Md Emon Hasan Portfolio](https://md-emon-hasan.github.io/My-Resume/)

## Overview

This repository contains a Google Colab notebook demonstrating:

1. **Conversation Management & Summarization**
   - Tracks user-assistant conversation history.
   - Supports truncation (last n turns, max characters, max words).
   - Automatic summarization after every k-th run.

2. **JSON Schema Classification & Extraction**
   - Uses OpenAI-style function calling (Groq API compatible) to extract structured information from chats.
   - Validates outputs using `jsonschema`.

## Setup

1. **Clone repository**
```bash
git clone https://github.com/Md-Emon-Hasan/Yardstick.git
cd ConversationManagement-Groq
```

2. **Install dependencies (Colab or local Python 3.10+)**

```bash
pip install openai jsonschema
```

3. **Provide Groq API Key (DO NOT COMMIT)**

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

or in Colab, use interactive input/getpass as shown in the notebook.

## Usage

* Open `notebook/Yardstick.ipynb` in Google Colab.
* Run all cells sequentially.
* Observe conversation history management, truncation, auto-summarization, and JSON schema extraction.

## Security Notes

* **Never commit API keys to GitHub.**
* Use GitHub Secrets or Colab runtime environment variables for safe API key handling.
