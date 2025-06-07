from ..LLMInterface import LLMInterface
from ..LLMEnums import HuggingFaceEnums, DocumentTypeEnum
from huggingface_hub import InferenceClient
import logging

class HuggingFaceProvider(LLMInterface):

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = InferenceClient(token=self.api_key)

        self.enums = HuggingFaceEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        
        if not self.client:
            self.logger.error("HuggingFace client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for HuggingFace was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        # Format chat history for HuggingFace models
        formatted_chat = []
        for message in chat_history:
            formatted_chat.append(message)

        # Add the current prompt
        formatted_chat.append(self.construct_prompt(prompt=prompt, role=HuggingFaceEnums.USER.value))

        try:
            # Using text generation API
            response = self.client.text_generation(
                model=self.generation_model_id,
                prompt=self.process_text(prompt),
                max_new_tokens=max_output_tokens,
                temperature=temperature,
            )

            if not response:
                self.logger.error("Error while generating text with HuggingFace")
                return None
            
            return response
        except Exception as e:
            self.logger.error(f"Error while generating text with HuggingFace: {e}")
            return None

    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("HuggingFace client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for HuggingFace was not set")
            return None
        
        processed_text = self.process_text(text)
        try:
            # Using feature extraction API
            embedding = self.client.feature_extraction(
                model=self.embedding_model_id,
                text=processed_text
            )
            
            if embedding is None:
                self.logger.error("Error while embedding text with HuggingFace")
                return None
                
            return embedding.tolist() if hasattr(embedding, 'tolist') else embedding
        except Exception as e:
            self.logger.error(f"Error while embedding text with HuggingFace: {e}")
            return None

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }