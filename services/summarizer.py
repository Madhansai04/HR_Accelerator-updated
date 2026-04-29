from services.llama_general import call_llm

def summarize(content):
    prompt = f"""
Explain this like a tutor.

Rules:
- Simple explanation
- Max 5 lines
- NO HTML tags
- NO <h1>, <p>, <br>, etc
- Plain text only

Content:
{content}
"""
    return call_llm(prompt)