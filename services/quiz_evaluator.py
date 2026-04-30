# services/quiz_evaluator.py
from services.llama_general import call_llm_quiz


def evaluate_quiz(content: str, quiz: str, answers: str) -> str:

    # Count actual subjective questions in the quiz
    subj_count = sum(1 for line in quiz.split("\n") if line.strip().startswith("Subjective"))

    # Build dynamic subjective feedback format
    if subj_count == 0:
        subj_format = "No subjective questions in this quiz."
    else:
        subj_format = "\n".join([f"- Q{i+1}: feedback on answer quality and what was missing"
                                  for i in range(subj_count)])

    prompt = f"""You are a detailed quiz evaluator for a retail analytics learning platform.

SECTION CONTENT (source of truth):
{content[:2000]}

QUIZ QUESTIONS:
{quiz}

USER ANSWERS:
{answers}

IMPORTANT: This quiz has exactly {subj_count} subjective question(s).
Do NOT mention or evaluate any subjective questions beyond that count.

EVALUATION RULES:
1. For MCQs — check if selected option is correct based on section content
2. For subjective — check if the concept is correctly understood, not exact wording
3. Give specific feedback on what was right and what was wrong
4. Be encouraging but honest
5. Only evaluate questions that actually exist in the quiz above

Return EXACTLY in this format:

MCQ Score: X out of Y

MCQ Feedback:
- Q1: Correct/Wrong — brief explanation of correct answer
- Q2: Correct/Wrong — brief explanation of correct answer
- Q3: Correct/Wrong — brief explanation of correct answer

Subjective Feedback:
{subj_format}

Weak Areas:
- area 1

What to Revise:
- specific topic 1

Overall: encouraging closing remark based on performance
"""
    return call_llm_quiz(prompt)