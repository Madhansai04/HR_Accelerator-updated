from services.llama_general import call_llm

def extract_jargon(content):
    prompt = f"""
Extract key jargon terms.

STRICT RULES:
- Return ONLY in this format:
 Term | Meaning
- No bullets
- No numbering
- No extra text

Content:
{content}
"""
    return call_llm(prompt)