class ChatMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, text):
        self.history.append({
            "role": "user",
            "content": [{"text": text}]
        })

    def add_assistant_message(self, text):
        self.history.append({
            "role": "assistant",
            "content": [{"text": text}]
        })

    def get_messages(self):
        return self.history

    def clear(self):
        self.history = []