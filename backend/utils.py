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

def convert_messages_into_string(messages, lastMessage):
    conversation = "System: You are a helpful assistant\n"

    if messages != []:
        for message in messages:
            if message[4] == 1:
                conversation += "Assistant: " + message[1] + "\n"
            else:
                conversation += "User: " + message[1] + "\n"
    
    conversation += "User: " + lastMessage + "\n"

    conversation += "Assistant: "

    return conversation

def get_generated_text(outputs, prompts) -> str:
    return outputs[0].replace(prompts[0], "").strip()