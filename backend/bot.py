import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os
from huggingface_hub import login

login('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')

from utils import convert_messages_into_string, get_generated_text


class Bot:

    def __init__(self):
        # Set the device
        self.gpu = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Set the model name
        model_name = "meta-llama/Llama-3.2-3B-Instruct"

        # Configure 4-bit quantization for the Llama model
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )

        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )
        print("Tokenizer loaded")

        # Configure the tokenizer to ensure padding is done correctly
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = 'left'

        # Load the model with quantization
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",  # Automatically maps the model across available devices
            quantization_config=quantization_config
        )
        print("Model loaded and quantized")

        # Move the model to evaluation mode
        self.model.eval()

        # Default generation arguments
        self.generate_kwargs = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "do_sample": True
        }

        print("Bot ready to chat")

    def generate(self, prompts: list) -> list:
        # Convert sentences into tokens
        input_tokens = self.tokenizer.batch_encode_plus(
            prompts,
            return_tensors="pt",
            padding=True
        )

        # Send the tokens to the model's device
        input_tokens = {key: tensor.to(self.model.device) for key, tensor in input_tokens.items()}

        # Generate the outputs
        output_tokens = self.model.generate(**input_tokens, **self.generate_kwargs)

        # Decode the tokens
        outputs = self.tokenizer.batch_decode(output_tokens, skip_special_tokens=True)

        return outputs

    def get_response(self, messages: list, lastMessage: str) -> str:
        # Convert the messages into a conversation
        prompts = [convert_messages_into_string(messages, lastMessage)]

        print("Prompts:", prompts)

        # Generate the response
        outputs = self.generate(prompts)

        print("Outputs:", outputs)

        generated_text = get_generated_text(outputs)

        print("Generated text:", generated_text)

        return generated_text

    def get_chat_name(self, firstMessage: str) -> str:
        templates = [
            f"You're a helpful assistant. Here's the first message of the user: '{firstMessage}'. Generate a 3-4 word title that describes this chat. Put the title beween quotation marks. Assistant :"
        ]

        outputs = self.generate(
            templates
            )

        print("Outputs:", outputs)

        generated_text = get_generated_text(outputs, is_for_title = True)

        print("Generated text:", generated_text)

        return generated_text
