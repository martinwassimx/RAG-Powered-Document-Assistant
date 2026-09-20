from typing import Any, Dict, List, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.utils.logging_config import logger


class RetrievalService:
    """Manages document chunk retrieval using ChromaDB and Sentence Transformers."""

    def __init__(self):
        self.chroma_path = settings.resolved_chroma_path
        self.collection_name = settings.COLLECTION_NAME
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.client: Optional[chromadb.ClientAPI] = None
        self.collection: Optional[chromadb.Collection] = None
        self.embedding_model: Optional[SentenceTransformer] = None
        self._is_initialized = False

    def initialize(self) -> None:
        """Initialize ChromaDB client and load the embedding model once."""
        if self._is_initialized:
            logger.info("RetrievalService is already initialized.")
            return

        logger.info(f"Connecting to ChromaDB at: {self.chroma_path}")
        self.chroma_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.chroma_path),
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Computer Science Educational Course Handouts"}
        )

        logger.info(f"Loading embedding model: {self.model_name}")
        self.embedding_model = SentenceTransformer(self.model_name)
        self._is_initialized = True

        total_chunks = self.get_total_chunks()
        logger.info(f"RetrievalService ready. Collection '{self.collection_name}' contains {total_chunks} chunks.")

    @property
    def is_ready(self) -> bool:
        return self._is_initialized and self.collection is not None and self.embedding_model is not None

    def get_total_chunks(self) -> int:
        if self.collection is not None:
            try:
                return self.collection.count()
            except Exception:
                return 0
        return 0

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Perform semantic similarity search for a user query."""
        if not self.is_ready:
            raise RuntimeError("RetrievalService is not initialized. Please ensure backend startup completed.")

        k = top_k if (top_k is not None and 1 <= top_k <= 20) else settings.TOP_K
        total_available = self.get_total_chunks()

        if total_available == 0:
            logger.warning("Vector store is empty! No chunks available for retrieval.")
            return []

        search_k = min(k, total_available)

        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]

        # Query ChromaDB collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=search_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else [{}] * len(docs)
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)
            ids = results["ids"][0] if "ids" in results and results["ids"] else [f"chunk_{i}" for i in range(len(docs))]

            for chunk_id, doc_text, meta, dist in zip(ids, docs, metas, distances):
                retrieved_chunks.append({
                    "chunk_id": chunk_id,
                    "document": meta.get("document", "Unknown Document"),
                    "page": int(meta.get("page", 1)),
                    "content": doc_text,
                    "distance": round(float(dist), 4) if dist is not None else None,
                    "snippet": doc_text[:200].replace("\n", " ") + "..." if len(doc_text) > 200 else doc_text
                })

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query[:40]}...'")
        return retrieved_chunks

    def format_context_for_prompt(self, chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks into structured context for LLM prompting."""
        if not chunks:
            return "No relevant context found."

        formatted_blocks = []
        for i, chunk in enumerate(chunks, start=1):
            block = (
                f"--- SOURCE [{i}]: {chunk['document']} (Page {chunk['page']}, Chunk: {chunk['chunk_id']}) ---\n"
                f"{chunk['content']}"
            )
            formatted_blocks.append(block)

        return "\n\n".join(formatted_blocks)


# Global singleton instance
retrieval_service = RetrievalService()
