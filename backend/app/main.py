from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.query import router as query_router
from app.core.config import settings
from app.services.generation import generation_service
from app.services.retrieval import retrieval_service
from app.utils.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to load heavy resources once at application startup."""
    logger.info("==================================================")
    logger.info("Initializing RAG Document Assistant Backend...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Vector Store Path: {settings.resolved_chroma_path}")
    logger.info(f"Ollama Target Host: {settings.OLLAMA_HOST}")
    logger.info(f"Ollama Target Model: {settings.OLLAMA_MODEL}")
    logger.info("==================================================")

    # Initialize ChromaDB vector store and SentenceTransformer embedding model
    try:
        retrieval_service.initialize()
    except Exception as exc:
        logger.error(f"Failed to initialize RetrievalService during startup: {str(exc)}")

    # Initialize Ollama generation client
    try:
        generation_service.initialize()
    except Exception as exc:
        logger.error(f"Failed to initialize GenerationService during startup: {str(exc)}")

    logger.info("Startup complete. Application ready to accept queries.")
    yield

    # Teardown logic if required
    logger.info("Shutting down RAG Document Assistant Backend...")


# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Production-style RAG (Retrieval-Augmented Generation) Document Assistant API. "
        "Built with FastAPI, ChromaDB, Sentence Transformers, and Ollama."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
origins = settings.cors_origins_list
logger.info(f"Configuring CORS with allowed origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if "*" not in origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred while processing your request."}
    )


# Root Endpoint
@app.get("/", tags=["General"], summary="API Root Overview")
async def root():
    return {
        "message": "Welcome to the RAG-Powered Document Assistant API",
        "docs_url": "/docs",
        "health_check": "/health",
        "version": settings.APP_VERSION
    }


# Include Routers
app.include_router(query_router)
