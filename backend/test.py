from bot import Bot

# Create a bot instance
chatbot = Bot()

# Sample messages to simulate a conversation
messages = [
    (1, "Hi! How can I assist you?", None, None, 1),
    (2, "Bonjour, peux-tu me répondre en français à partir de maintenant ?", None, None, 0),
    (3, "Oui, comment puis-je vous aider ?", None, None, 1)
]

# last_message = input("User:")
last_message = "User: can tell me a nice story about bear ?"

# Get the response from the bot
response = chatbot.get_response(messages, last_message)

# Print the bot's response
print("Bot:", response)