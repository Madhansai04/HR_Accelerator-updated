from services.llama_general import call_llm
import re

def estimate_time(content):
    prompt = f"""
Return ONLY one answer.

Estimate time to learn this.

STRICT:
- Only return like: 5 mins OR 10 mins OR 15 mins
- No explanation
- No extra text

Content:
{content}
"""
    response = call_llm(prompt)

    text = response.strip()

    match = re.search(r"\d+\s*mins", text)

    return match.group(0) if match else "10 mins"