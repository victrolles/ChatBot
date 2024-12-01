import re

def print_outputs(outputs):
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    print("-" * 80)

def convert_messages_into_conversation(messages, lastMessage):
    conversation = []

    introduction = {
        "role": "system",
        "content": "You are a helpful assistant"
    }

    lastMessage_dict = {
        "role": "user",
        "content": lastMessage
    }
    
    conversation.append(introduction)

    for message in messages:
        if message[4] == 1:
            conversation.append({"role": "assistant",
                                "content": message[1]})
        else:
            conversation.append({"role": "user",
                            "content": message[1]})
            
    conversation.append(lastMessage_dict)

    return conversation

# def convert_messages_into_chat(messages, lastMessage):
#     conversation = []

#     if messages != []:
#         for message in messages:
#             if message[4] == 1:
#                 conversation += "Assistant: " + message[1] + "\n"
#             else:
#                 conversation += "User: " + message[1] + "\n"
    
#     conversation += "User: " + lastMessage + "\n"

#     conversation += "Assistant: "

#     return conversation

# messages = [
#     (1, "Hi! How can I assist you?", None, None, 1),
#     (2, "Bonjour, peux-tu me répondre en français à partir de maintenant ?", None, None, 0),
#     (3, "Oui, comment puis-je vous aider ?", None, None, 1)
# ]

def convert_messages_into_string(messages, lastMessage):
    conversation = "System: You are a helpful assistant. Try to be clear and very concise, do not generate more than 512 characters by message.\n"

    if messages != []:
        for message in messages:
            if message[4] == 1:
                conversation += "Assistant: " + message[1] + "\n"
            else:
                conversation += "User: " + message[1] + "\n"
    
    conversation += "User: " + lastMessage + "\n"

    conversation += "Assistant : "

    return conversation

def nettoyer_chaine(texte):
    # Trouver la position de "Assistant :"
    position = texte.find("Assistant : ")
    if position != -1:
        # Retourner la chaîne à partir de ce qui suit "Assistant :"
        return texte[position + len("Assistant : "):]
    return texte  # Retourner la chaîne originale si "Assistant :" n'est pas trouvé

def extraire_contenu(texte):
    # Utiliser une expression régulière pour capturer le contenu entre les premiers guillemets
    pattern = r'"(.*?)"'
    match = re.search(pattern, texte)
    if match:
        return match.group(1)  # Retourner le contenu capturé
    return None  # Retourner None si aucun match n'est trouvé

def get_generated_text(outputs, is_for_title = False) -> str:
    if is_for_title:
        return extraire_contenu(outputs[0])
    return nettoyer_chaine(outputs[0])