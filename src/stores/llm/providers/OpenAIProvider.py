from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging
from typing import List, Union

class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, api_url: str=None,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.api_url if self.api_url and len(self.api_url) else None
        )

        self.enums = OpenAIEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                  temperature: float = None):

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature is not None else self.default_generation_temperature

        # Construct full chat history with system prompt
        full_chat_history = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers legal questions based strictly on the provided legal documents."
            },
            {
                "role": "user",
                "content": prompt.strip()
            }
        ]

        # Include prior chat history if needed (optional)
        full_chat_history.extend(chat_history)

        # Log what we're about to send
        self.logger.info(f"Sending chat completion request with model: {self.generation_model_id}")
        self.logger.debug(f"Chat history:\n{full_chat_history}")
        self.logger.debug(f"Max tokens: {max_output_tokens}, Temperature: {temperature}")

        try:
            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=full_chat_history,
                max_tokens=max_output_tokens,
                temperature=temperature
            )

            # Log full response for debugging
            self.logger.debug(f"OpenAI response: {response}")

            if not response or not response.choices:
                self.logger.error("No choices returned in OpenAI response.")
                return None

            message = response.choices[0].message
            if not message or not message.content:
                self.logger.error("Message content in OpenAI response is empty.")
                return None

            return message.content.strip()

        except Exception as e:
            self.logger.exception("Exception during OpenAI chat completion")
            return None



    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if isinstance(text, str):
            text = [text]

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text,
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None

        return [ rec.embedding for rec in response.data ]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt,
        }
    