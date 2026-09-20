from fastapi import APIRouter, HTTPException, status
from typing import List

from app.core.config import settings
from app.schemas.query import HealthResponse, QueryRequest, QueryResponse, SourceItem
from app.services.generation import generation_service
from app.services.retrieval import retrieval_service
from app.utils.logging_config import logger

router = APIRouter(tags=["RAG Document Assistant"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health and Diagnostics Check",
    description="Inspect system operational status, vector store chunk count, and Ollama connectivity."
)
async def health_check():
    """Verify backend health, ChromaDB readiness, and Ollama LLM availability."""
    vector_ready = retrieval_service.is_ready
    chunk_count = retrieval_service.get_total_chunks() if vector_ready else 0

    llm_info = generation_service.check_reachability()
    llm_ready = llm_info.get("reachable", False)

    overall_status = "healthy" if (vector_ready and llm_ready) else "degraded"

    return HealthResponse(
        status=overall_status,
        environment=settings.APP_ENV,
        vector_store={
            "initialized": vector_ready,
            "collection": settings.COLLECTION_NAME,
            "total_chunks": chunk_count,
            "storage_path": str(settings.resolved_chroma_path)
        },
        llm=llm_info,
        embedding_model=settings.EMBEDDING_MODEL_NAME
    )


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Query Document Assistant",
    description="Retrieve relevant chunks from indexed documents and generate a grounded, cited answer using Ollama."
)
async def query_documents(request: QueryRequest):
    """Execute end-to-end RAG pipeline for a user query."""
    logger.info(f"Received query: '{request.question}' (top_k override: {request.top_k})")

    # Step 1: Retrieval
    try:
        retrieved_chunks = retrieval_service.retrieve(
            query=request.question,
            top_k=request.top_k
        )
    except Exception as exc:
        logger.error(f"Retrieval error: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving document context from the vector store."
        )

    # If no chunks were retrieved (e.g. empty vector store)
    if not retrieved_chunks:
        return QueryResponse(
            answer="I could not find any relevant information in the provided documents.",
            sources=[],
            model=settings.OLLAMA_MODEL,
            retrieval_count=0
        )

    # Step 2: Format Context & Citations
    context = retrieval_service.format_context_for_prompt(retrieved_chunks)
    sources: List[SourceItem] = [
        SourceItem(
            document=c["document"],
            page=c["page"],
            chunk_id=c["chunk_id"],
            relevance_score=c["distance"],
            snippet=c["snippet"]
        )
        for c in retrieved_chunks
    ]

    # Step 3: LLM Generation
    try:
        answer = generation_service.generate_answer(
            question=request.question,
            context=context
        )
    except Exception as exc:
        logger.error(f"Generation error: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"The LLM service (Ollama) was unavailable or failed to generate a response: {str(exc)}"
        )

    return QueryResponse(
        answer=answer,
        sources=sources,
        model=settings.OLLAMA_MODEL,
        retrieval_count=len(retrieved_chunks)
    )
