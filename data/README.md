# Dataset Documentation: Computer Science Educational Corpus

## Domain Overview
The dataset selected for this RAG-Powered Document Assistant consists of **University Computer Science Educational Documents**. It represents foundational academic material taught across undergraduate and graduate computer science courses.

This domain provides a rigorous testing ground for document retrieval and question answering because it contains:
- Exact technical definitions (e.g., ACID properties, Big-O bounds, Coffman conditions)
- Comparative concepts (e.g., TCP vs. UDP, Threads vs. Processes, B-Trees vs. Hash Indexes)
- Multi-step procedural explanations (e.g., TCP 3-way handshake, LRU page replacement, Event Loop cycles)
- Complex numerical/algorithmic bounds requiring precise, grounded answers without hallucinations.

---

## Document Corpus (`data/raw/`)

| File Name | Topic Area | Target Pages | Key Concepts Covered |
|:---|:---|:---:|:---|
| `cs101_algorithms_complexity.pdf` | Algorithms & Data Structures | 3 | Asymptotic notations ($O, \Omega, \Theta$), Quicksort & Mergesort time/space complexity, Dynamic Programming vs Greedy algorithms, Hash collision resolution. |
| `cs102_operating_systems.pdf` | Operating Systems Fundamentals | 3 | Process states and PCB, CPU scheduling (Round Robin, SRTF), Virtual Memory and Paging, Page Fault handling, Coffman conditions for Deadlock. |
| `cs103_database_acid_indexing.pdf` | Database Management Systems | 3 | Relational normalization (1NF to BCNF), ACID transaction guarantees, Concurrency anomalies (Dirty Read, Non-repeatable Read, Phantom), B-Tree & LSM storage structures. |
| `cs104_computer_networks.pdf` | Computer Networks & Protocols | 3 | OSI 7-Layer vs TCP/IP model, TCP 3-way handshake and 4-way termination, Congestion control algorithms, DNS recursive resolution, TLS 1.3 cryptographic handshake. |
| `cs105_python_concurrency.pdf` | Python Concurrency & Async | 3 | CPython Global Interpreter Lock (GIL), Multithreading vs Multiprocessing trade-offs, `asyncio` event loop architecture, Coroutines, Tasks, and Race condition prevention. |

---

## Adding Custom Documents
To ingest your own course materials, textbooks, or enterprise documentation into the assistant:

1. Place your target `.pdf` files into `data/raw/`.
2. Ensure the documents have searchable text layers (run an inspection using `pypdf` or `pdfplumber` to verify text extraction without OCR).
3. Execute the notebook `notebooks/rag_pipeline.ipynb` or trigger the ingestion pipeline.
4. The chunks will be automatically generated, embedded with `all-MiniLM-L6-v2`, and indexed into ChromaDB at `backend/data/vector_store/`.
5. Restart or reload the FastAPI backend to query your newly indexed documents.
