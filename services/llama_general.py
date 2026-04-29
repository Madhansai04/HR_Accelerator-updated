from backend.config.config import client
import os
from dotenv import load_dotenv

# ✅ THIS LINE IS MISSING
load_dotenv()

MODEL_ID = os.getenv("LLAMA_GENERAL", "meta.llama3-8b-instruct-v1:0")

def call_llm(prompt):
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    )

    return response["output"]["message"]["content"][0]["text"]