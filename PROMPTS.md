# AI Usage Log

This file records the AI-assisted development process.

## Product concept
Interview OS is an adaptive interview agent. It evaluates candidate answers,
tracks weaknesses, changes question difficulty, remembers interview history,
and produces a candidate profile.

## Prompt 1 — Product architecture
Design an interview agent that behaves differently from a normal chatbot.
The system should evaluate each answer, identify weaknesses, adapt the next
question, and produce a final candidate profile.

## Prompt 2 — Adaptive questioning
Design a strategy for selecting the next interview question using the previous
answer, detected weaknesses, role, difficulty, and previous questions.

## Prompt 3 — Evaluation
Create a structured JSON evaluation for technical correctness, clarity,
reasoning, strengths, weaknesses and recommended focus.

## Prompt 4 — Final report
Generate a candidate profile that summarizes strengths, weaknesses, behavioral
patterns and a strategy for the next interview.

## Human decisions
- Chose Streamlit for rapid UI development.
- Chose SQLite for a simple local history store.
- Chose provider abstraction so the demo can run with OpenAI or local Ollama.
- Kept the MVP focused on adaptive interviewing rather than adding unrelated
  features.
