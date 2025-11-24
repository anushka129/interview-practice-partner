# Interview Practice Partner — Assignment Submission

**Project:** Interview Practice Partner (conversational AI agent)  
**Purpose:** Mock interview practice with feedback for different roles (software engineer, product manager, sales, etc.).  

---

## What's included
- `app.py` — Flask backend that calls OpenAI (if `OPENAI_API_KEY` set) or runs an offline demo mode.
- `templates/index.html` — Simple chat UI with voice input using Web Speech API.
- `static/script.js` — Frontend logic to interact with backend.
- `requirements.txt` — Python dependencies.
- `README.md` — This file.

---

## Quick setup (local)
1. Clone repository or copy files.
2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\\Scripts\\activate     # Windows
pip install -r requirements.txt
```
3. (Optional) Set OpenAI API key as environment variable:
```bash
export OPENAI_API_KEY="sk-..."
# Windows PowerShell:
# $env:OPENAI_API_KEY = "sk-..."
```
4. Run the app:
```bash
python app.py
```
5. Open `http://127.0.0.1:5000` in your browser. If you did not set an API key, the app runs in offline demo mode that simulates basic behavior.

---

## Architecture & Design Decisions
- **Why Flask?** Lightweight, easy to run locally and deploy to Heroku/Render. Keeps the submission simple and focused on conversation quality.
- **Agentic behavior:** The system prompt instructs the model to ask follow-ups, request clarifications, and provide structured feedback (communication, technical, structure, improvement tips).
- **Voice support:** Web Speech API on the frontend for quick voice input during the demo video (works in Chrome).
- **Offline demo mode:** To ensure the demo works even without an API key, the backend detects missing `OPENAI_API_KEY` and uses simple heuristics to emulate an interview flow.
- **Model choice:** Uses `gpt-4o-mini` in code — change to your preferred model (gpt-4o, gpt-4, gpt-4o-mini) based on availability and quota.
- **Conversation history:** Frontend sends the conversation history so the model can ask follow-ups based on prior answers.

---

## How this meets the assignment requirements
- **Mock interviews for specific roles:** role selector and system prompt configure role-specific behavior.
- **Follow-up questions:** model is instructed to follow up based on user answers — conversation history preserved.
- **Post-interview feedback:** "Get feedback" button sends the conversation to the model in `feedback` mode.
- **Interaction mode:** Chat UI with optional voice input; simple to adapt to voice-only flows.
