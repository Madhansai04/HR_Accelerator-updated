from services.llama_general import call_llm

def evaluate_quiz(content, quiz, answers):
    prompt = f"""
You are an evaluator.

Quiz:
{quiz}

User answers:
{answers}

Evaluate:

1. MCQ answers (score)
2. Subjective answers (quality)

Return:
- MCQ score (e.g., 2/3)
- Subjective feedback
- Weak areas
- Suggestions to improve

Keep it very short and clear.
"""
    return call_llm(prompt)