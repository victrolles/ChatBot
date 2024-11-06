import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils import convert_messages_into_string, get_generated_text

class Bot:

    def __init__(self):

        # Set the device
        self.gpu = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Set the model name
        model_name = "bigscience/bloomz-560m"
        # model_name = "bigscience/bloomz-1b7"
        # model_name = "bigscience/bloomz-3b"
        # model_name = "bigscience/bloomz-7b1"
        # model_name = "meta-llama/Llama-2-7b-hf"
        # model_name = "meta-llama/Llama-2-13b-hf"
        # model_name = "google/flan-t5-large"


        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )
        print("Tokenizer loaded")

        # Configure the tokenizer to ensure padding is done right
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = 'left'

        # Load the model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        print("Model loaded")
        
        # Move the model to the GPU
        self.model.to(self.gpu)
        print("Model moved to the GPU")

        # Move the model to eval mode
        self.model.eval()

        self.generate_kwargs = {
            "max_new_tokens": 512,
            "temperature": 0.9,
            "do_sample": True
        }


        print("Bot ready to chat")

    def generate(self, prompts: list) -> list:

        # Convert sentences in tokens
        input_tokens = self.tokenizer.batch_encode_plus(
            prompts,
            return_tensors="pt",
            padding = True
        )

        # print("input_tokens", input_tokens)

        # Send the tokens to the gpus
        for t in input_tokens:
            if torch.is_tensor(input_tokens[t]):
                input_tokens[t] = input_tokens[t].to(self.gpu)

        # Generate the outputs
        output_tokens = self.model.generate(**input_tokens, **self.generate_kwargs)

        # print("output_tokens", output_tokens)

        # Decode the tokens
        outputs = self.tokenizer.batch_decode(output_tokens, skip_special_tokens=True)

        # print("outputs", outputs)

        return outputs


    def get_response(self, messages: list, lastMessage: str) -> str:
        
        # Convert the messages into a conversation
        prompts = [convert_messages_into_string(messages, lastMessage)]

        # Generate the response by the llm
        outputs = self.generate(prompts)

        # return only the generated part of the new prompt
        return get_generated_text(outputs, prompts)
    
    def get_chat_name(self, firstMessage: int) -> str:

        templates = [
            f"You're a helpful assistant, he will ask you questions and you will answer them. Here is his first message: '{firstMessage}'. Can you generate a 2 or 3 word title which describes this chat? Answer :",
        ]

        outputs = self.generate(templates)

        return get_generated_text(outputs, templates)