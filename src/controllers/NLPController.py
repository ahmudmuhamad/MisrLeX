from .BaseController import BaseController
from models.db_schemas import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        # Ensure DocumentTypeEnum is imported, e.g., from stores.llm.LLMEnums import DocumentTypeEnum
        # You might want to add logging for skipped items:
        # import logging
        # logger = logging.getLogger(__name__)

        prepared_texts = []
        prepared_metadata = []
        prepared_vectors = []
        prepared_record_ids = []

        if not self.embedding_client:
            # logger.error(f"Embedding client not configured for project {project.project_id}.")
            return False # Cannot proceed without embedding client

        for chunk_data, chunk_id_val in zip(chunks, chunks_ids):
            text_to_embed = chunk_data.chunk_text
            
            vector = self.embedding_client.embed_text(
                text=text_to_embed,
                document_type=DocumentTypeEnum.DOCUMENT.value 
            )

            # Check if the vector is valid (not None, is a list, and not empty)
            if vector and isinstance(vector, list) and len(vector) > 0:
                prepared_texts.append(text_to_embed)
                prepared_metadata.append(chunk_data.chunk_metadata)
                prepared_vectors.append(vector)
                prepared_record_ids.append(chunk_id_val)
            else:
                # logger.warning(f"Failed to generate/invalid embedding for chunk_id {chunk_id_val} in project {project.project_id}. Skipping this chunk.")
                pass # Optionally log skipped chunk

        # step3: create collection if not exists
        # Ensure embedding_size is available on the embedding_client
        if self.embedding_client.embedding_size is None:
            # logger.error(f"Embedding size not set on embedding client for project {project.project_id}.")
            return False

        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # step4: insert into vector db only if there's valid data to insert
        if not prepared_vectors:
            # logger.info(f"No valid embeddings to insert for project {project.project_id} after filtering.")
            return True # Successfully processed, though nothing new was inserted.

        insert_success = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=prepared_texts,
            metadata=prepared_metadata,
            vectors=prepared_vectors,
            record_ids=prepared_record_ids,
        )

        return insert_success

    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector
        vector = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        # step3: do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results
    
    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": doc.text,
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
        })

        # step3: Construct Generation Client Prompts
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history
