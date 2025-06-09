from ..LLMInterface import LLMInterface
from ..LLMEnums import JinaAIEnums, DocumentTypeEnum
from sentence_transformers import SentenceTransformer
import logging

class JinaAIProvider(LLMInterface):

    def __init__(self, api_key: str = None, # API key might not be needed for local model
                       default_input_max_characters: int = 8192, # Jina v3 supports up to 8192 tokens
                       default_generation_max_output_tokens: int = 1000, # Not used for embeddings
                       default_generation_temperature: float = 0.1): # Not used for embeddings
        
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        # These are not strictly necessary for an embedding-only provider but kept for interface consistency
        self.default_generation_max_output_tokens = default_generation_max_output_tokens 
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None # Not used for embeddings

        self.embedding_model_id = None
        self.embedding_size = None
        self.client = None # Will be the SentenceTransformer model

        self.enums = JinaAIEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        # This provider focuses on embeddings, so generation model is not applicable
        self.logger.warning("JinaAIProvider is an embedding provider, set_generation_model is not applicable.")
        self.generation_model_id = None

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        try:
            # Load the model locally
            self.client = SentenceTransformer(model_name_or_path=self.embedding_model_id, trust_remote_code=True)
            # Verify embedding dimension if possible, though SentenceTransformer handles it
            # actual_embedding_size = self.client.get_sentence_embedding_dimension()
            # if actual_embedding_size != self.embedding_size:
            #     self.logger.warning(f"Provided embedding_size {self.embedding_size} does not match model's actual size {actual_embedding_size}. Using model's size.")
            #     self.embedding_size = actual_embedding_size
            self.logger.info(f"Successfully loaded JinaAI embedding model: {self.embedding_model_id} with embedding size: {self.embedding_size}")
        except Exception as e:
            self.logger.error(f"Failed to load JinaAI embedding model {self.embedding_model_id}: {e}")
            self.client = None

    def process_text(self, text: str):
        # Jina v3 can handle long contexts, but good to have a truncation safeguard
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        # This provider focuses on embeddings, so text generation is not applicable
        self.logger.warning("JinaAIProvider is an embedding provider, generate_text is not applicable.")
        return None

    def embed_text(self, text: str, document_type: str = None): # document_type is not used by sentence-transformers for jina v3
        if not self.client:
            self.logger.error("JinaAI embedding model was not set or failed to load")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for JinaAI was not set")
            return None
        
        processed_text = self.process_text(text)
        try:
            embedding = self.client.encode(processed_text)
            embedding = self.client.encode(processed_text)

            if isinstance(embedding, list):
                embedding = np.array(embedding)

            if embedding.ndim != 1:
                raise ValueError(f"Expected 1D embedding, got shape: {embedding.shape}")

            return embedding.tolist()
 # Ensure it's a list
        except Exception as e:
            self.logger.error(f"Error while embedding text with JinaAI: {e}")
            return None

    def construct_prompt(self, prompt: str, role: str):
        # Not applicable for an embedding-only provider using sentence-transformers
        # Kept for interface consistency
        self.logger.warning("JinaAIProvider is an embedding provider, construct_prompt is not directly used for embeddings.")
        return {
            "role": role, # or some JinaAI specific role if it were a chat model
            "content": self.process_text(prompt)
        }