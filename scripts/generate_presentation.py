"""
Script to generate a professional, modern 16:9 PowerPoint presentation
for the RAG-Powered Document Assistant project using python-pptx.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path: str):
    prs = Presentation()
    # Set 16:9 widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Deep Slate / Tech Dark Theme
    BG_DARK = RGBColor(15, 23, 42)        # #0f172a (Deep navy/slate)
    CARD_BG = RGBColor(30, 41, 59)        # #1e293b (Card navy)
    CARD_BORDER = RGBColor(51, 65, 85)    # #334155
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38bdf8 (Cyan accent)
    ACCENT_INDIGO = RGBColor(99, 102, 241)# #6366f1 (Indigo accent)
    TEXT_WHITE = RGBColor(248, 250, 252)  # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94a3b8
    ACCENT_GREEN = RGBColor(74, 222, 128) # #4ade80

    blank_layout = prs.slide_layouts[6] # Blank slide layout

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="RAG-POWERED DOCUMENT ASSISTANT"):
        # Category / Pill Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_CYAN

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title="", title_color=ACCENT_CYAN):
        # Card shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Inner text frame
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(10)
        return tf

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.8), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    bar.line.fill.background()

    # Title box
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11.7), Inches(2.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "RAG-Powered Document Assistant"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "A Production-Grade, Privacy-First Academic Q&A System with Page-Level Citations"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_before = Pt(8)

    # Metadata Card
    card_tf = add_card(s1, Inches(0.8), Inches(4.7), Inches(11.73), Inches(1.8), "PROJECT OVERVIEW & SPECIFICATION")
    bullets = [
        ("Core Track: ", "Text-Based Document Retrieval-Augmented Generation (RAG) with Citations"),
        ("Architecture: ", "FastAPI Backend + Sentence Transformers + Persistent ChromaDB + Local Ollama LLM + Streamlit UI"),
        ("Privacy & Rigor: ", "100% Offline execution, Zero External API Keys, Hallucination-Resistant Grounding"),
        ("Dataset: ", "University CS Academic Course Handouts (15 Pages, 45 Chunks across 5 Domains)")
    ]
    for bold_prefix, text in bullets:
        bp = card_tf.add_paragraph()
        run1 = bp.add_run()
        run1.text = bold_prefix
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = ACCENT_INDIGO
        run2 = bp.add_run()
        run2.text = text
        run2.font.size = Pt(13)
        run2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_background(s2)
    add_header(s2, "Problem Statement & Engineering Motivation", "BACKGROUND & CONTEXT")

    c1 = add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "The LLM Hallucination Trap", RGBColor(239, 68, 68))
    for line in [
        "Standard LLMs generate confident yet entirely fabricated statements.",
        "Zero verifiable references or page-level citations for technical claims.",
        "Out-of-domain questions yield misleading answers rather than honest refusals.",
        "Unusable for academic study where precision and attribution are mandatory."
    ]:
        p = c1.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    c2 = add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "Privacy & Cloud Risks", RGBColor(245, 158, 11))
    for line in [
        "Proprietary textbooks, student notes, and exams uploaded to cloud APIs risk data leakage.",
        "Dependency on external APIs (OpenAI, Anthropic) introduces latency, quotas, and recurring subscription costs.",
        "Network dependency renders assistants unavailable in air-gapped or offline exam environments."
    ]:
        p = c2.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    c3 = add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "The Grounded RAG Solution", ACCENT_GREEN)
    for line in [
        "Retrieval-Augmented Generation: Answers derived strictly from indexed course documents.",
        "Granular Page Citations: Every claim tagged with document name and exact page number.",
        "Zero-Hallucination Refusal: Explicit fallback when information is missing from documents.",
        "100% Local Pipeline: ChromaDB + Ollama running entirely on host workstation."
    ]:
        p = c3.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: System Architecture & End-to-End Pipeline
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_background(s3)
    add_header(s3, "End-to-End System Architecture", "SYSTEM DESIGN")

    p1 = add_card(s3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8), "1. Offline Ingestion & Indexing Pipeline", ACCENT_CYAN)
    ingestion_steps = [
        ("Raw Educational PDFs: ", "Source course handouts in data/raw/*.pdf (15 pages across 5 subjects)."),
        ("PyPDF Extraction: ", "Clean vector-stream text parsing with whitespace normalization."),
        ("Sliding Window Chunking: ", "Chunk size 800 chars (~140 words) with 150 chars overlap."),
        ("Sentence Transformers: ", "all-MiniLM-L6-v2 produces dense 384-dimensional semantic embeddings."),
        ("ChromaDB Persistence: ", "Vectors and rich metadata saved to backend/data/vector_store/ for instant cold-starts.")
    ]
    for title, desc in ingestion_steps:
        bp = p1.add_paragraph()
        r1 = bp.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(6)

    p2 = add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "2. Online Serving & Inference Pipeline", ACCENT_INDIGO)
    serving_steps = [
        ("Streamlit Chat UI: ", "Student asks natural language questions, inspects interactive citation badges."),
        ("FastAPI Backend: ", "High-performance async server validates input via Pydantic QueryRequest."),
        ("Retrieval Service: ", "Encodes query, executes cosine similarity search in ChromaDB, fetches Top-K chunks."),
        ("Grounded Prompt Builder: ", "Assembles strict system context, instructions, and source metadata."),
        ("Local Ollama Engine: ", "Runs llama3:latest locally on GPU, generating grounded answers."),
        ("Structured JSON: ", "Returns answer alongside verifiable {document, page, chunk_id, relevance_score}.")
    ]
    for title, desc in serving_steps:
        bp = p2.add_paragraph()
        r1 = bp.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: Academic Dataset & Domain Corpus
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_background(s4)
    add_header(s4, "Domain Corpus & Document Specification", "DATASET DESIGN")

    # Left summary card
    dc = add_card(s4, Inches(0.8), Inches(1.8), Inches(3.8), Inches(4.8), "Corpus Highlights", ACCENT_CYAN)
    for line in [
        "15 Total Academic Pages",
        "45 Semantic Chunks",
        "5 Foundational CS Topics",
        "Pure digital vector PDFs (100% extractable without OCR degradation)",
        "Carefully formatted definitions, theorems, and trade-off tables"
    ]:
        p = dc.add_paragraph()
        p.text = "✔ " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # Right 5 courses cards
    courses = [
        ("CS101: Algorithms & Complexity", "Big-O, Omega, Theta, Master Theorem, Quicksort vs Mergesort, Hash Collisions", "9 Chunks (3 Pages)"),
        ("CS102: Operating Systems", "Process States, PCB, CPU Scheduling, Virtual Memory, TLB, Deadlock Coffman Conditions", "9 Chunks (3 Pages)"),
        ("CS103: Database Management Systems", "Relational Normalization (1NF-BCNF), ACID Properties, Isolation Levels, B+ Trees", "9 Chunks (3 Pages)"),
        ("CS104: Computer Networks", "OSI vs TCP/IP, TCP 3-Way Handshake & Teardown, Flow & Congestion Control, DNS", "9 Chunks (3 Pages)"),
        ("CS105: Python Concurrency", "CPython GIL Mechanics, Threading vs Multiprocessing, Asyncio Event Loop, Race Conditions", "9 Chunks (3 Pages)"),
    ]
    top_pos = 1.8
    for c_title, c_topics, c_meta in courses:
        cc = add_card(s4, Inches(4.9), Inches(top_pos), Inches(7.6), Inches(0.85), "", ACCENT_CYAN)
        p = cc.paragraphs[0]
        r1 = p.add_run()
        r1.text = c_title + "  "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE

        r_badge = p.add_run()
        r_badge.text = f"[{c_meta}]\n"
        r_badge.font.size = Pt(11)
        r_badge.font.color.rgb = ACCENT_CYAN

        r2 = p.add_run()
        r2.text = c_topics
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

        top_pos += 0.98

    # =========================================================================
    # SLIDE 5: Chunking & Text Extraction Strategy
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_background(s5)
    add_header(s5, "Chunking Strategy & Parameter Engineering", "DATA PREPROCESSING")

    k1 = add_card(s5, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "Chunk Size: 800 Chars", ACCENT_CYAN)
    for line in [
        "Captures complete semantic units: Academic definitions (e.g. 4 Coffman conditions) span 400-700 characters.",
        "Avoids premature fragmentation that destroys technical nuance.",
        "Translates to ~180 WordPiece tokens, fitting cleanly inside the model's 256-token limit."
    ]:
        p = k1.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    k2 = add_card(s5, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "Chunk Overlap: 150 Chars", ACCENT_INDIGO)
    for line in [
        "Provides a 20% sliding window buffer across chunk boundaries.",
        "Prevents boundary severance: Multi-sentence theorems that cross arbitrary cutoffs remain discoverable in both adjacent chunks.",
        "Reduces retrieval false-negatives during vector proximity calculations."
    ]:
        p = k2.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    k3 = add_card(s5, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "Rich Metadata Schema", ACCENT_GREEN)
    for line in [
        "Granular Traceability: Each chunk retains document name, page number, and unique chunk_id.",
        "Deterministic Citations: Allows the Streamlit UI to display verified page badges for every retrieved fact.",
        "Zero Index Leakage: Fully persisted in ChromaDB metadata schema."
    ]:
        p = k3.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 6: Embeddings & Vector Database
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_background(s6)
    add_header(s6, "Embeddings & ChromaDB Vector Store", "VECTOR RETRIEVAL")

    v1 = add_card(s6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8), "Sentence Transformers (all-MiniLM-L6-v2)", ACCENT_CYAN)
    emb_points = [
        ("Architecture: ", "6-layer MiniLM transformer mapping sentences to a 384-dimensional dense semantic vector space."),
        ("Speed & Efficiency: ", "Ultra-lightweight (~80MB model weight), runs blazingly fast on both CPU and GPU."),
        ("Semantic Quality: ", "Trained specifically for cosine-similarity semantic search, capturing nuanced technical terminology across Computer Science domains."),
        ("Deterministic Output: ", "Identical embeddings for repeated queries ensure consistent retrieval ranks.")
    ]
    for pfx, txt in emb_points:
        bp = v1.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    v2 = add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Persistent ChromaDB Engine", ACCENT_INDIGO)
    chroma_points = [
        ("Storage Architecture: ", "Persisted directly to disk at backend/data/vector_store/ using SQLite + HNSW index."),
        ("Zero Re-indexing Overhead: ", "FastAPI loads the persistent collection at startup; no costly re-indexing on container or server restart."),
        ("Cosine Similarity Metric: ", "Normalized vectors enable high-precision nearest-neighbor queries with sub-millisecond retrieval latency."),
        ("Collection Metadata: ", "Maintains collection 'cs_course_documents' with 45 chunks and schema manifest.")
    ]
    for pfx, txt in chroma_points:
        bp = v2.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: Grounded Prompt Engineering
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_background(s7)
    add_header(s7, "Strict Grounding & Prompt Engineering", "PROMPT DESIGN")

    pr1 = add_card(s7, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8), "System Prompt Architecture", ACCENT_CYAN)
    prompt_text = (
        "You are an expert academic assistant for Computer Science courses.\n\n"
        "STRICT GROUNDING RULES:\n"
        "1. Answer the question using ONLY the provided context passages below.\n"
        "2. Do NOT use prior knowledge or extrapolate beyond the text.\n"
        "3. For every factual claim, cite the document name and page number [Doc, Page X].\n"
        "4. If the context does not contain the answer, you MUST state verbatim:\n"
        "   \"I could not find this information in the provided documents.\""
    )
    p = pr1.add_paragraph()
    p.text = prompt_text
    p.font.name = "Consolas"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(226, 232, 240)

    pr2 = add_card(s7, Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.8), "Key Engineering Outcomes", ACCENT_GREEN)
    outcomes = [
        ("Elimination of Confabulation: ", "The LLM cannot invent explanations or pretend knowledge about unindexed materials."),
        ("Granular Attribution: ", "Every assertion is linked directly to course lecture notes for immediate academic verification."),
        ("Explicit Fallback Mechanism: ", "Tested against historical and medical questions; reliably yields grounded refusals without evasive banter."),
        ("Token-Optimized Context: ", "Top-K parameter limits prompt size, ensuring inference completes within 2-4 seconds on local GPUs.")
    ]
    for pfx, txt in outcomes:
        bp = pr2.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: Local LLM Serving via Ollama
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_background(s8)
    add_header(s8, "Local LLM Inference with Ollama", "LOCAL AI INFERENCE")

    o1 = add_card(s8, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "Why Ollama?", ACCENT_CYAN)
    for line in [
        "100% Offline & Private: Zero telemetry, zero external cloud dependencies.",
        "GPU Acceleration: Automatic CUDA / Vulkan offloading for sub-second token generation.",
        "Model Agnostic: Seamless switching between llama3:latest and phi3:mini via simple environment variable.",
        "Production REST API: Clean HTTP client integration with configurable timeouts."
    ]:
        p = o1.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    o2 = add_card(s8, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "Llama 3 (8B) Capabilities", ACCENT_INDIGO)
    for line in [
        "State-of-the-art reasoning and instruction following.",
        "Strict adherence to negative constraints (refusal rules).",
        "Exceptional synthetic summarization of technical CS concepts (operating systems, networking, databases).",
        "2.2 GB quantized footprint fits comfortably on standard consumer GPUs."
    ]:
        p = o2.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    o3 = add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "Resilience & Fallbacks", ACCENT_GREEN)
    for line in [
        "Health Endpoint Diagnostics: FastAPI continuously checks if Ollama service is reachable on port 11434.",
        "Configurable Timeouts: Prevents hanging threads during heavy generation workloads.",
        "Clean Error Handling: Returns structured 503 Service Unavailable when the model service is offline."
    ]:
        p = o3.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 9: FastAPI Backend Service
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_background(s9)
    add_header(s9, "FastAPI Production Backend Architecture", "BACKEND SERVICE")

    b1 = add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8), "Architectural Highlights", ACCENT_CYAN)
    backend_bullets = [
        ("Lifespan Event Management: ", "Loads heavy SentenceTransformer model and ChromaDB client once into application state at startup, eliminating cold-start per-query latency."),
        ("Pydantic Schema Validation: ", "QueryRequest strictly validates question string (rejects empty/whitespace strings) and bounds top_k (1 to 10)."),
        ("Cross-Origin Resource Sharing (CORS): ", "Configurable middleware permits secure communication from Streamlit UI."),
        ("Structured Logging: ", "Centralized logging capturing query latency, retrieved chunk counts, and model inference metrics.")
    ]
    for pfx, txt in backend_bullets:
        bp = b1.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    b2 = add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "REST API Endpoints", ACCENT_INDIGO)
    api_bullets = [
        ("GET /health: ", "Monitors ChromaDB collection, total chunk count, storage directory, and Ollama reachable status with model availability."),
        ("POST /query: ", "Accepts {question, top_k}, retrieves semantic passages, invokes Ollama generation, and returns {answer, sources, model, retrieval_count}."),
        ("GET /docs & /redoc: ", "Interactive Swagger and ReDoc documentation for immediate interactive testing."),
        ("HTTP 422 Handling: ", "Returns detailed validation error messages for invalid or malformed payloads.")
    ]
    for pfx, txt in api_bullets:
        bp = b2.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 10: Streamlit Interactive Frontend
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_background(s10)
    add_header(s10, "Streamlit Frontend User Experience", "USER INTERFACE")

    u1 = add_card(s10, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "Real-Time System Health", ACCENT_CYAN)
    for line in [
        "Live status pill in header displays connected backend status.",
        "Diagnostic drawer shows indexed chunk count (45 chunks) and active LLM model.",
        "Automatic reconnection banner if backend or Ollama server goes offline."
    ]:
        p = u1.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    u2 = add_card(s10, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "Conversational Chat Feed", ACCENT_INDIGO)
    for line in [
        "Clean, intuitive chat history matching modern messaging standards.",
        "Quick-start prompt chips for instant testing across all CS subjects.",
        "Real-time typing spinner indicating vector search and generation progress."
    ]:
        p = u2.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    u3 = add_card(s10, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "Expandable Citation Cards", ACCENT_GREEN)
    for line in [
        "Every answer displays expandable badges for each cited document chunk.",
        "Displays Document Name, Page Number, and Cosine Relevance Score.",
        "Full excerpt preview allows students to verify answers against the original text."
    ]:
        p = u3.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 11: Evaluation & Benchmark Results
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_background(s11)
    add_header(s11, "Evaluation Matrix & Hallucination Resistance", "EMPIRICAL EVALUATION")

    # Table of Evaluation Results
    rows, cols = 7, 4
    left, top, width, height = Inches(0.8), Inches(1.8), Inches(11.73), Inches(4.8)
    table_shape = s11.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(4.5)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(1.83)

    headers = ["Evaluation Query", "Expected Document & Page", "Retrieval Quality", "Result"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = ACCENT_CYAN

    eval_data = [
        ("What are the four Coffman conditions for a deadlock?", "cs102_operating_systems.pdf (P.3)", "Top-1 (Score: 0.38)", "PASSED (Grounded)"),
        ("Explain the TCP 3-way handshake process.", "cs104_computer_networks.pdf (P.2)", "Top-1 (Score: 0.34)", "PASSED (Grounded)"),
        ("Difference between B-Tree and B+ Tree indexing?", "cs103_database_acid_indexing.pdf (P.3)", "Top-1 (Score: 0.36)", "PASSED (Grounded)"),
        ("Why does CPython employ a GIL and how does it affect CPU tasks?", "cs105_python_concurrency.pdf (P.1)", "Top-1 (Score: 0.32)", "PASSED (Grounded)"),
        ("What are the therapeutic indications for Metformin? (Out of Domain)", "None (Unrelated Domain)", "Filtered / Refused", "PASSED (Refusal)"),
        ("What were the causes of the French Revolution in 1789? (Out of Domain)", "None (Unrelated Domain)", "Filtered / Refused", "PASSED (Refusal)"),
    ]

    for row_idx, row in enumerate(eval_data, start=1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_DARK
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            elif col_idx == 0:
                p.font.color.rgb = TEXT_WHITE
            else:
                p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 12: Automated Pytest Suite
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_background(s12)
    add_header(s12, "Automated Testing & Quality Assurance", "TEST AUTOMATION")

    t1 = add_card(s12, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8), "9 Passing Automated Tests (pytest)", ACCENT_CYAN)
    test_cases = [
        ("test_health_check_returns_200", "Verifies vector store initialization and LLM reachability status."),
        ("test_query_missing_body_returns_422", "Ensures requests lacking a payload are rejected with 422 Unprocessable Entity."),
        ("test_query_empty_string_returns_422", "Validates that empty string questions trigger Pydantic value errors."),
        ("test_query_whitespace_only_returns_422", "Guards against questions containing only spaces/tabs."),
        ("test_query_too_short_returns_422", "Enforces minimum character length requirements."),
        ("test_query_invalid_top_k_returns_422", "Prevents memory exhaustion from excessive top_k parameters."),
        ("test_query_happy_path_with_mocked_llm", "Tests complete retrieval-to-generation pipeline with mocked LLM."),
        ("test_query_retrieves_correct_context", "Confirms ChromaDB vector search pulls relevant document chunks.")
    ]
    for t_name, t_desc in test_cases:
        bp = t1.add_paragraph()
        r1 = bp.add_run()
        r1.text = "✔ " + t_name + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_GREEN
        r2 = bp.add_run()
        r2.text = "   " + t_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(4)

    t2 = add_card(s12, Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.8), "Testing Philosophy", ACCENT_INDIGO)
    for pfx, txt in [
        ("Fast Execution: ", "Unit tests isolate external dependencies using HTTPX TestClient and mocked generation services, finishing in under 3 seconds."),
        ("Regression Protection: ", "Prevents breaking API contracts, schema drifts, or validation bugs before deployment."),
        ("CI/CD Ready: ", "Configured with backend/pytest.ini for headless pipeline execution.")
    ]:
        bp = t2.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(12)

    # =========================================================================
    # SLIDE 13: Containerization & DevOps
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_slide_background(s13)
    add_header(s13, "Containerization & Multi-Service Deployment", "DEVOPS & DEPLOYMENT")

    d1 = add_card(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8), "Docker Multi-Container Setup", ACCENT_CYAN)
    for pfx, txt in [
        ("FastAPI Container (rag_backend): ", "Packages Python 3.12 slim image, mounts persistent vector store, and maps port 8000."),
        ("Streamlit Container (rag_frontend): ", "Serves the reactive UI on port 8501 with dependent startup on backend."),
        ("Host LLM Gateway: ", "Leverages host.docker.internal:11434 to route LLM generation requests to host GPU-accelerated Ollama."),
        ("Persistent Volumes: ", "Vector store volume mounting prevents indexing duplication inside containers.")
    ]:
        bp = d1.add_paragraph()
        r1 = bp.add_run()
        r1.text = pfx
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TEXT_WHITE
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_MUTED
        bp.space_after = Pt(10)

    d2 = add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "One-Command Orchestration", ACCENT_INDIGO)
    code_box = (
        "# Build and start all services in isolated containers:\n"
        "docker compose up --build\n\n"
        "# Services exposed:\n"
        "Frontend UI: http://localhost:8501\n"
        "Backend API: http://localhost:8000\n"
        "Swagger Docs: http://localhost:8000/docs\n\n"
        "# Clean teardown:\n"
        "docker compose down"
    )
    p = d2.add_paragraph()
    p.text = code_box
    p.font.name = "Consolas"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(226, 232, 240)

    # =========================================================================
    # SLIDE 14: Future Enhancements & Roadmap
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_slide_background(s14)
    add_header(s14, "Future Enhancements & Technical Roadmap", "ROADMAP")

    f1 = add_card(s14, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "Hybrid Search (Dense + Sparse)", ACCENT_CYAN)
    for line in [
        "Combine BM25 keyword matching with dense SentenceTransformer vectors.",
        "Use Reciprocal Rank Fusion (RRF) to merge ranks.",
        "Improves retrieval for exact keyword code snippets, variable names, and acronyms."
    ]:
        p = f1.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    f2 = add_card(s14, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "Cross-Encoder Re-Ranking", ACCENT_INDIGO)
    for line in [
        "Introduce a two-stage retrieval pipeline with bge-reranker-large.",
        "Re-ranks candidate Top-10 chunks down to Top-3 high-precision passages.",
        "Significantly enhances complex comparative query answering."
    ]:
        p = f2.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    f3 = add_card(s14, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "Streaming Token Inference", ACCENT_GREEN)
    for line in [
        "Implement Server-Sent Events (SSE) in FastAPI backend.",
        "Stream LLM tokens dynamically to Streamlit interface using st.write_stream.",
        "Decreases perceived Time-To-First-Token (TTFT) to under 400 milliseconds."
    ]:
        p = f3.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 15: Conclusion & Q&A
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_slide_background(s15)

    # Large Center Card
    conc_card = add_card(s15, Inches(1.5), Inches(1.2), Inches(10.33), Inches(5.1), "Project Summary & Key Takeaways", ACCENT_CYAN)
    bullets_final = [
        ("Complete End-to-End Delivery: ", "Engineered, tested, and validated all 5 phases of the production RAG requirements."),
        ("Zero-Hallucination Grounding: ", "Strict prompt engineering forces the model to cite specific document pages and refuse out-of-domain queries."),
        ("100% Privacy-Preserving Architecture: ", "Zero external API keys, zero cloud egress, and complete on-premise execution."),
        ("Production Engineering Standards: ", "Lifespan loading, persistent ChromaDB index, Pydantic validation, 9 automated tests, and Docker readiness.")
    ]
    for pfx, txt in bullets_final:
        bp = conc_card.add_paragraph()
        r1 = bp.add_run()
        r1.text = "✔ " + pfx
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = ACCENT_GREEN
        r2 = bp.add_run()
        r2.text = txt
        r2.font.size = Pt(14)
        r2.font.color.rgb = TEXT_WHITE
        bp.space_after = Pt(10)

    p_qa = conc_card.add_paragraph()
    p_qa.text = "\nThank You! Open for Questions & Live Demonstration."
    p_qa.font.bold = True
    p_qa.font.size = Pt(18)
    p_qa.font.color.rgb = ACCENT_CYAN
    p_qa.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_pptx = os.path.join(out_dir, "RAG_Document_Assistant_Presentation.pptx")
    create_presentation(target_pptx)
