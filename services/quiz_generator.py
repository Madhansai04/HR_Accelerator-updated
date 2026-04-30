from services.llama_general import call_llm_quiz

def generate_smart_quiz(content, user_summary):
    prompt = f"""
You are a strict quiz generator.

Content:
{content}

User summary:
{user_summary}

Task:
1. Identify weak areas
2. Generate EXACTLY:
   - 3 MCQs
   - 2 Subjective questions

STRICT FORMAT (DO NOT BREAK):

Q1: question
A) option
B) option
C) option
D) option

Q2: question
A) option
B) option
C) option
D) option

Q3: question
A) option
B) option
C) option
D) option

Subjective 1: question
Subjective 2: question


RULES:
- No extra text
- No explanations
- No bullets
- No markdown
- No headings like ***
- Follow format EXACTLY
"""

    return call_llm_quiz(prompt)
