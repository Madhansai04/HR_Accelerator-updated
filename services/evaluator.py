from services.llama_general import call_llm


def evaluate(section_text, user_answer):
    prompt = f"""
You are an expert evaluator for a learning platform.

CONTENT:
{section_text[:2000]}

USER ANSWER:
{user_answer}

Evaluate the user's understanding.

Return your response STRICTLY in this format:

Score: X/10

Correct Points:
- point 1
- point 2

Missing Points:
- point 1
- point 2

Improvement Suggestions:
- suggestion 1
- suggestion 2
"""

    return call_llm(prompt)