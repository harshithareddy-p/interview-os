import os
import json
import requests


def get_provider():
    return os.getenv("AI_PROVIDER", "demo").lower()


def ask_ai(prompt, system_prompt="You are an expert technical interviewer."):
    """
    Generate an AI response.

    Supports:
    - OpenAI-compatible API through environment variables
    - Demo fallback when no API is configured
    """

    provider = get_provider()

    # -----------------------------
    # DEMO MODE
    # -----------------------------
    if provider == "demo":
        return demo_response(prompt)

    # -----------------------------
    # OPENAI-COMPATIBLE API
    # -----------------------------
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return demo_response(prompt)

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": os.getenv(
                        "OPENAI_MODEL",
                        "gpt-4o-mini"
                    ),
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7
                },
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"AI service unavailable. Using demo interviewer.\n\n{demo_response(prompt)}"

    return demo_response(prompt)


def demo_response(prompt):
    """
    Offline fallback so the application can still demonstrate
    the adaptive interview experience.
    """

    prompt_lower = prompt.lower()

    if "python" in prompt_lower:
        return (
            "In Python, explain the difference between a list and a tuple. "
            "Give one practical situation where you would choose each."
        )

    if "database" in prompt_lower or "sql" in prompt_lower:
        return (
            "Imagine you have a table containing millions of users. "
            "How would you improve the performance of a query filtering "
            "users by email?"
        )

    if "algorithm" in prompt_lower or "dsa" in prompt_lower:
        return (
            "You are given an array of integers. Explain how you would "
            "find two numbers that add up to a target value. "
            "Start with a simple approach and then improve it."
        )

    if "project" in prompt_lower:
        return (
            "Tell me about a technical project you built. "
            "What problem did it solve, what was your contribution, "
            "and what technical challenge did you face?"
        )

    return (
        "Tell me about a challenging technical problem you solved. "
        "Explain your approach, the decisions you made, and the result."
    )


def generate_question(candidate, previous_answers=None):
    """
    Generate the next adaptive interview question.
    """

    previous_answers = previous_answers or []

    role = candidate.get("role", "Software Engineer")
    skills = candidate.get("skills", "Python and DSA")
    difficulty = candidate.get("difficulty", "Intermediate")

    if not previous_answers:
        return (
            f"You are interviewing for a {role} position.\n\n"
            f"Candidate skills: {skills}\n"
            f"Difficulty: {difficulty}\n\n"
            "Ask the candidate a technical question that tests "
            "fundamental understanding."
        )

    last_answer = previous_answers[-1]

    return (
        f"The candidate is interviewing for {role}.\n"
        f"Skills: {skills}\n"
        f"Difficulty: {difficulty}\n\n"
        f"Their previous answer was:\n{last_answer}\n\n"
        "Identify one weakness, missing concept, or interesting point "
        "in that answer and ask ONE targeted follow-up question."
    )


def evaluate_answer(question, answer):
    """
    Evaluate a candidate answer and return structured feedback.
    """

    prompt = f"""
Evaluate this technical interview answer.

Question:
{question}

Candidate Answer:
{answer}

Return JSON with exactly these fields:

{{
    "score": 0,
    "strength": "one sentence",
    "weakness": "one sentence",
    "follow_up": "one question"
}}

Score from 0 to 10.
"""

    result = ask_ai(
        prompt,
        system_prompt=(
            "You are a strict but fair technical interviewer. "
            "Evaluate answers based on correctness, clarity, "
            "reasoning and depth."
        )
    )

    try:
        return json.loads(result)
    except Exception:
        return {
            "score": 6,
            "strength": "The candidate attempted the question.",
            "weakness": "The answer needs more technical depth.",
            "follow_up": "Can you explain your reasoning with an example?"
        }


def generate_report(candidate, answers):
    """
    Generate the final Interview DNA report.
    """

    formatted_answers = "\n\n".join(
        [
            f"Question: {item.get('question', '')}\n"
            f"Answer: {item.get('answer', '')}\n"
            f"Score: {item.get('score', 0)}"
            for item in answers
        ]
    )

    prompt = f"""
Create a candidate interview report.

Candidate:
{candidate}

Interview:
{formatted_answers}

Identify:

1. Overall technical level
2. Strongest skill
3. Weakest skill
4. Repeated mistakes
5. Communication quality
6. Recommended next topic
7. Overall score

Return a concise report.
"""

    report = ask_ai(
        prompt,
        system_prompt=(
            "You are an expert interview evaluator. "
            "Give honest, constructive and specific feedback."
        )
    )

    return {
        "overall_score": calculate_score(answers),
        "candidate_pattern": report,
        "recommendation": "Practice the weakest detected topic before the next interview."
    }


def calculate_score(answers):
    """
    Calculate average interview score.
    """

    if not answers:
        return 0

    scores = []

    for item in answers:
        try:
            scores.append(float(item.get("score", 0)))
        except Exception:
            pass

    if not scores:
        return 0

    return round((sum(scores) / len(scores)) * 10)
