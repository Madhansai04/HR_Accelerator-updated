from services.llama_general import call_llm

def teach(section_text):
    prompt = f"""
You are a person with the strong domain knowledge and share the knowledge like a tutor.

Explain the following content in a very simple and clear way:
  -Some of the key terms will not be known to user try to cover them to.
  -Train the user to the level that he/she can be equal knowledge with the domain experts.

{section_text[:3000]}
"""
    return call_llm(prompt)
