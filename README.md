# 🎯 Interview OS

> Build the interviewer, not the interview.

Interview OS is an adaptive AI interviewer that builds a lightweight
"Interview DNA" profile from a candidate's answers.

## Core idea

A normal interview bot does:

Question → Answer → Random Question

Interview OS does:

Question → Analyze → Detect Weakness → Adapt → Follow-up → Remember

## Features

- Adaptive AI interviewer
- Answer-level scoring
- Weakness detection
- Difficulty adaptation
- Candidate Interview DNA
- Interview history
- Next-interview strategy
- Interviewer quality score
- OpenAI or local Ollama provider

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

For OpenAI:

```bash
set OPENAI_API_KEY=YOUR_KEY
streamlit run app.py
```

For PowerShell:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY"
streamlit run app.py
```

For Ollama:

1. Install Ollama.
2. Pull a model, for example `ollama pull llama3.2:3b`.
3. Start Ollama.
4. Run the app.
5. Select `Ollama` in the sidebar.

## Hackathon demo flow

1. Open Home.
2. Start an interview.
3. Choose Python Developer.
4. Select 5 questions.
5. Give a strong answer to one question.
6. Give a deliberately weak answer to another.
7. Show that the next question targets the weakness.
8. Finish the interview.
9. Show Interview DNA.
10. Show interviewer quality and next interview strategy.

## Important

Create meaningful commits during the hackathon and keep PROMPTS.md updated
with the prompts actually used. Do not present an imported prebuilt repository
as hackathon work.
