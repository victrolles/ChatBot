class Bot:

    def __init__(self):
        self.model = "llama"
        print("Bot created")

    def get_response(self, message: str) -> str:
        return "I am a chatbot"