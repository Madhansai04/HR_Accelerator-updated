# services/evaluator.py
#
# Evaluates user's understanding of a section.
# Uses 70B model for better judgment.
# Scores based on CONCEPTS understood, not exact wording.

from services.llama_general import call_llm_quiz


def evaluate(section_text: str, user_answer: str) -> str:
    prompt = f"""You are a fair but strict evaluator for a retail analytics learning platform.

SECTION CONTENT (source of truth):
{section_text[:2000]}

USER ANSWER:
{user_answer}

EVALUATION RULES:

1. RELEVANCE CHECK FIRST:
   - If answer is gibberish, random characters, or completely unrelated to retail/section → Score: 0/10. Stop.
   - If answer is copied word-for-word from content → Score: 0/10. State plagiarism detected.

2. SCORING BASIS:
   - Score based on CONCEPTS and IDEAS understood, NOT exact wording.
   - If user explains a concept correctly in their own words → give full credit.
   - If user partially understands a concept → give partial credit.
   - Do NOT penalize for using different words as long as meaning is correct.
   - Do NOT give credit for concepts not related to this section.

3. SCORING GUIDE:
   - 0/10  → Irrelevant, copied, or gibberish
   - 1-3/10 → Mentions 1-2 concepts vaguely or incorrectly
   - 4-5/10 → Shows basic understanding of some key concepts
   - 6-7/10 → Good understanding of most concepts in own words
   - 8-9/10 → Strong understanding of nearly all concepts clearly explained
   - 10/10  → Complete, accurate understanding of all key concepts

4. FEEDBACK RULES:
   - Be specific — mention exact concepts the user got right or wrong
   - Be encouraging — acknowledge effort and correct understanding
   - Be actionable — give clear suggestions on what to revisit

Return EXACTLY in this format, nothing else:

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
    return call_llm_quiz(prompt)