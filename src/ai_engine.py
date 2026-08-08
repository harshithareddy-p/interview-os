import os
import json
import requests


class AIEngine:

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "demo").lower()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ask(self, prompt, system_prompt=None):

        if self.provider != "openai" or not self.api_key:
            return self.demo_response(prompt)

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                            or "You are an expert technical interviewer."
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

        except Exception:
            return self.demo_response(prompt)

    def demo_response(self, prompt):

        prompt = prompt.lower()

        if "python" in prompt:

            return (
                "In Python, what is the difference between a list "
                "and a tuple? Give a practical example of when you "
                "would use each."
            )

        if "sql" in prompt or "database" in prompt:

            return (
                "Suppose you have a database containing millions "
                "of users. How would you improve the performance "
                "of a query that searches users by email?"
            )

        if "dsa" in prompt or "algorithm" in prompt:

            return (
                "You are given an array of integers and a target. "
                "How would you find two numbers that add up to "
                "the target? Explain a brute-force approach and "
                "then an optimized approach."
            )

        return (
            "Tell me about a challenging technical problem you "
            "solved. Explain your approach, the decisions you "
            "made, and the result."
        )

    def generate_question(self, candidate, previous_answers=None):

        previous_answers = previous_answers or []

        role = candidate.get(
            "role",
            "Software Engineer"
        )

        skills = candidate.get(
            "skills",
            "Python and DSA"
        )

        difficulty = candidate.get(
            "difficulty",
            "Intermediate"
        )

        if not previous_answers:

            prompt = f"""
You are interviewing a candidate for a {role} position.

Skills:
{skills}

Difficulty:
{difficulty}

Ask ONE technical interview question.
"""

        else:

            last_answer = previous_answers[-1]

            prompt = f"""
You are interviewing a candidate for a {role} position.

Their previous answer was:

{last_answer}

Identify one weakness or missing concept.

Ask ONE targeted follow-up question.
"""

        return self.ask(
            prompt,
            "You are an adaptive technical interviewer."
        )

    def evaluate_answer(self, question, answer):

        prompt = f"""
Evaluate this technical interview answer.

Question:
{question}

Candidate answer:
{answer}

Give:
- score from 0 to 10
- strength
- weakness
- follow-up question
"""

        result = self.ask(
            prompt,
            "You are a strict but fair technical interviewer."
        )

        return {
            "score": 7,
            "strength": "The candidate demonstrated reasonable understanding.",
            "weakness": "The answer could include deeper technical reasoning.",
            "follow_up": "Can you explain your approach with a concrete example?"
        }

    def generate_report(self, candidate, answers):

        if not answers:

            return {
                "overall_score": 0,
                "candidate_pattern": "No interview answers recorded.",
                "recommendation": "Complete an interview first."
            }

        scores = []

        for answer in answers:

            try:
                scores.append(
                    float(answer.get("score", 0))
                )
            except Exception:
                pass

        if scores:

            score = round(
                (sum(scores) / len(scores)) * 10
            )

        else:

            score = 0

        report_prompt = f"""
Create an interview performance report.

Candidate:
{candidate}

Answers:
{json.dumps(answers, indent=2)}

Identify:
1. Strongest skill
2. Weakest skill
3. Repeated mistakes
4. Communication quality
5. Recommended next topic
6. Overall assessment
"""

        report = self.ask(
            report_prompt,
            "You are an expert interview evaluator."
        )

        return {
            "overall_score": score,
            "candidate_pattern": report,
            "recommendation": (
                "Practice the weakest detected area "
                "before the next interview."
            )
        }
