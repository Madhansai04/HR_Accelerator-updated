from services.llama_general import call_llama_general
from services.llama_code import call_llama_code

def route(messages):
    user_text = messages[-1]["content"][0]["text"].lower()

    # smarter keyword routing
    coding_keywords = [
        "code", "program", "bug", "error",
        "java", "python", "c++", "algorithm"
    ]

    if any(word in user_text for word in coding_keywords):
        print("Using CODE model")
        return call_llama_code(messages)
    else:
        print("Using GENERAL model")
        return call_llama_general(messages)