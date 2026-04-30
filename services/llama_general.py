# services/llama_general.py
#
# Two LLM functions:
# call_llm()      → 8B model  → fast tasks (summary, jargon, time)
# call_llm_quiz() → 70B model → smart tasks (evaluate, quiz generate, quiz evaluate)

from backend.config.config import client
from backend.config.settings import LLAMA_GENERAL, LLAMA_CODE


def call_llm(prompt: str) -> str:
    """Fast 8B model — summaries, time estimation, jargon."""
    print(f"[LLM] GENERAL model ({LLAMA_GENERAL})")
    response = client.converse(
        modelId=LLAMA_GENERAL,
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    return response["output"]["message"]["content"][0]["text"]


def call_llm_quiz(prompt: str) -> str:
    """Smart 70B model — evaluation, quiz generation, quiz evaluation."""
    print(f"[LLM] QUIZ model ({LLAMA_CODE})")
    response = client.converse(
        modelId=LLAMA_CODE,
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    return response["output"]["message"]["content"][0]["text"]