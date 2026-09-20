import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_pdf(filename: str, title: str, pages_content: list):
    pdf_path = RAW_DATA_DIR / filename
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'DocCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=10
    )

    story = []
    
    for page_idx, (page_heading, sections) in enumerate(pages_content, start=1):
        if page_idx == 1:
            story.append(Paragraph(title, title_style))
            story.append(Paragraph(f"Department of Computer Science & Engineering | Academic Handout", ParagraphStyle(
                'Sub', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor("#64748b"), spaceAfter=15
            )))
        
        story.append(Paragraph(f"Page {page_idx}: {page_heading}", h2_style))
        story.append(Spacer(1, 6))
        
        for heading, body in sections:
            if heading:
                story.append(Paragraph(heading, ParagraphStyle(
                    'DocH3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor("#0f766e"), spaceBefore=6, spaceAfter=4
                )))
            if isinstance(body, list):
                for paragraph_text in body:
                    story.append(Paragraph(paragraph_text, body_style))
            elif isinstance(body, str):
                if body.startswith("NOTE:") or body.startswith("DEFINITION:"):
                    story.append(Paragraph(body, callout_style))
                else:
                    story.append(Paragraph(body, body_style))
            story.append(Spacer(1, 4))
            
        if page_idx < len(pages_content):
            story.append(PageBreak())

    doc.build(story)
    print(f"Generated: {pdf_path} ({len(pages_content)} pages)")


def generate_all_documents():
    print("Generating University Computer Science Course Handouts...")

    # Document 1: Algorithms & Complexity
    cs101_pages = [
        (
            "Foundations of Asymptotic Analysis & Sorting",
            [
                ("1.1 Asymptotic Notations and Formal Definitions", [
                    "Asymptotic analysis evaluates algorithmic resource consumption as input size n approaches infinity. Three primary notations form the foundation of algorithm analysis:",
                    "• Big-O Notation (O): Represents an asymptotic upper bound. Formally, f(n) = O(g(n)) if there exist positive constants c and n0 such that 0 <= f(n) <= c * g(n) for all n >= n0. It characterizes worst-case performance.",
                    "• Big-Omega Notation (Omega): Represents an asymptotic lower bound. Formally, f(n) = Omega(g(n)) if there exist positive constants c and n0 such that 0 <= c * g(n) <= f(n) for all n >= n0.",
                    "• Big-Theta Notation (Theta): Represents an asymptotically tight bound. Formally, f(n) = Theta(g(n)) if and only if f(n) = O(g(n)) and f(n) = Omega(g(n)).",
                    "Common complexity tiers ordered by growth rate: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)."
                ]),
                ("1.2 Comparison-Based Sorting Algorithms", [
                    "DEFINITION: Quicksort is a divide-and-conquer sorting algorithm. It selects a pivot element, partitions the array into sub-arrays of elements less than and greater than the pivot, and recursively sorts the sub-arrays. On average, Quicksort runs in O(n log n) time and requires O(log n) auxiliary stack space. In the worst case (e.g. sorted input with deterministic first/last element pivot), Quicksort degrades to O(n^2) time.",
                    "Mergesort consistently guarantees O(n log n) running time in best, average, and worst cases by dividing the array into halves, recursively sorting both, and merging the sorted sublists. However, standard array-based Mergesort requires O(n) additional auxiliary memory for merging buffers. Mergesort is a stable sorting algorithm.",
                    "Heapsort constructs a binary heap data structure from the input array and iteratively extracts the maximum (or minimum) root element. Heapsort runs in guaranteed O(n log n) time in all cases and sorts in-place with O(1) auxiliary space, though it is not a stable sort."
                ])
            ]
        ),
        (
            "Recurrence Relations, Master Theorem & Algorithmic Paradigms",
            [
                ("1.3 Recurrence Relations and the Master Theorem", [
                    "Divide-and-conquer algorithms often yield recurrence relations of the form: T(n) = a * T(n/b) + f(n), where a >= 1 represents the number of recursive subproblems, b > 1 represents the subproblem division factor, and f(n) represents the cost of dividing and combining.",
                    "The Master Theorem provides asymptotic bounds across three principal cases by comparing f(n) against n^(log_b(a)):",
                    "• Case 1: If f(n) = O(n^(log_b(a) - epsilon)) for some epsilon > 0, then T(n) = Theta(n^(log_b(a))). The leaf work dominates.",
                    "• Case 2: If f(n) = Theta(n^(log_b(a)) * (log n)^k) for k >= 0, then T(n) = Theta(n^(log_b(a)) * (log n)^(k+1)). Work is evenly distributed across recursion levels.",
                    "• Case 3: If f(n) = Omega(n^(log_b(a) + epsilon)) for epsilon > 0 and regularity condition a * f(n/b) <= c * f(n) holds for c < 1, then T(n) = Theta(f(n)). The root work dominates."
                ]),
                ("1.4 Dynamic Programming versus Greedy Method", [
                    "Dynamic Programming (DP) solves optimization problems by decomposing them into overlapping subproblems and exhibiting optimal substructure. Solutions to subproblems are stored in a lookup table to eliminate redundant calculations. Top-down DP utilizes memoization, while bottom-up DP utilizes iterative tabulation.",
                    "The Greedy Method constructs a global solution by making a locally optimal choice at each step without reconsidering prior decisions. A greedy algorithm yields an optimal solution only if the problem exhibits both optimal substructure and the greedy-choice property (e.g. Fractional Knapsack, Dijkstra's Single-Source Shortest Path, Huffman Encoding). In contrast, the 0/1 Knapsack problem requires Dynamic Programming because the greedy choice does not guarantee global optimality."
                ])
            ]
        ),
        (
            "Hash Tables, Collision Resolution & Amortized Analysis",
            [
                ("1.5 Hash Tables and Collision Handling Strategies", [
                    "A Hash Table maps keys to bucket indices using a hash function h(k). Under the Simple Uniform Hashing Assumption (SUHA), each key is equally likely to hash into any of the m available slots.",
                    "Collision resolution methods fall into two major categories:",
                    "1. Separate Chaining: Each bucket holds a linked list or self-balancing binary search tree of colliding entries. The load factor alpha = n / m can exceed 1.0. Search and deletion cost average O(1 + alpha).",
                    "2. Open Addressing: All elements reside directly within the hash table array. When a collision occurs, alternative slots are probed systematically until an empty bucket is encountered. Load factor alpha cannot exceed 1.0. Probing methods include:",
                    "   - Linear Probing: h(k, i) = (h'(k) + i) mod m. Suffers from Primary Clustering where contiguous blocks of occupied slots grow and degrade search performance.",
                    "   - Quadratic Probing: h(k, i) = (h'(k) + c1*i + c2*i^2) mod m. Avoids primary clustering but can suffer from Secondary Clustering.",
                    "   - Double Hashing: h(k, i) = (h1(k) + i * h2(k)) mod m. Offers near-ideal pseudo-random probing, provided h2(k) is relatively prime to m.",
                    "Rehashing doubles table capacity and re-inserts all existing keys when load factor alpha exceeds a predefined threshold (typically 0.75), yielding amortized O(1) insertion time."
                ])
            ]
        )
    ]
    build_pdf("cs101_algorithms_complexity.pdf", "CS101: Algorithms and Computational Complexity", cs101_pages)

    # Document 2: Operating Systems
    cs102_pages = [
        (
            "Process Lifecycle, Threads & CPU Scheduling",
            [
                ("2.1 Process Lifecycle and Process Control Block (PCB)", [
                    "A process is a program in execution, consisting of program code (text segment), program counter, stack (temporary local variables and return addresses), data segment (global variables), and heap (dynamically allocated memory).",
                    "The operating system maintains a Process Control Block (PCB) for each process containing: Process ID (PID), Process State, CPU registers, CPU scheduling priority, memory-management information (page tables), and I/O status information.",
                    "Process states transition through: New -> Ready -> Running -> Waiting (Blocked) -> Terminated.",
                    "A Context Switch occurs when the CPU scheduler switches execution from one process to another. The OS saves the current state in the active PCB and restores the saved state of the scheduled PCB. Context switching represents pure system overhead because no useful user computation occurs during the transition.",
                    "Threads (lightweight processes) within the same process share code, data, open files, and address space, but each thread retains its own thread ID, program counter, register set, and private stack."
                ]),
                ("2.2 CPU Scheduling Algorithms", [
                    "• First-Come, First-Served (FCFS): Non-preemptive. Suffers from the Convoy Effect where short CPU-burst processes wait behind a long CPU-burst process, severely degrading average turnaround time.",
                    "• Shortest Job First (SJF) & Shortest Remaining Time First (SRTF): Preemptive (SRTF) or non-preemptive (SJF). Provably optimal in minimizing average waiting time, but susceptible to process starvation if short jobs continuously arrive.",
                    "• Round Robin (RR): Preemptive scheduling designed for time-sharing systems. Each process is allocated a fixed time quantum q. If the process does not complete within q, it is preempted and returned to the tail of the ready queue. If q is excessively large, RR degenerates into FCFS; if q is too small, context-switch overhead dominates."
                ])
            ]
        ),
        (
            "Virtual Memory, Paging Architecture & Replacement Algorithms",
            [
                ("2.3 Virtual Memory and Paging", [
                    "Virtual memory decouples user logical address space from physical memory. The Memory Management Unit (MMU) translates logical addresses composed of a page number (p) and offset (d) into physical frame numbers (f) using a per-process Page Table.",
                    "To accelerate address translation, CPUs employ a high-speed associative hardware cache called the Translation Lookaside Buffer (TLB).",
                    "Effective Memory Access Time (EMAT) is computed as: EMAT = h * (t_tlb + t_mem) + (1 - h) * (t_tlb + 2 * t_mem), where h is the TLB hit ratio, t_tlb is TLB access latency, and t_mem is main memory access latency.",
                    "A Page Fault exception occurs when a referenced page is marked invalid (not present in physical RAM). The OS traps to kernel mode, initiates disk I/O to swap in the requested page from backing store, updates the page table entry, and restarts the faulting instruction."
                ]),
                ("2.4 Page Replacement Algorithms", [
                    "When physical memory is exhausted and a page fault occurs, the OS must select a victim frame to evict using a page replacement policy:",
                    "• First-In, First-Out (FIFO): Evicts the oldest loaded page. FIFO is vulnerable to Belady's Anomaly, where increasing the number of allocated physical frames leads to an increase in the total number of page faults.",
                    "• Optimal Page Replacement (OPT / MIN): Evicts the page that will not be used for the longest future duration. OPT cannot be implemented in general-purpose OS kernels because future memory reference strings are unknown; it serves as a theoretical performance upper bound.",
                    "• Least Recently Used (LRU): Evicts the page that has not been referenced for the longest past interval. LRU is a stack algorithm and is mathematically immune to Belady's Anomaly.",
                    "• Clock Algorithm (Second Chance): Practical approximation of LRU using a single reference bit per frame and a rotating circular pointer."
                ])
            ]
        ),
        (
            "Deadlocks, Coffman Conditions & Concurrency Synchronization",
            [
                ("2.5 Deadlocks and the Four Coffman Conditions", [
                    "DEFINITION: A deadlock is a state where a set of processes are blocked because each process holds a resource and waits for another resource held by another process in the set. A deadlock can arise if and only if ALL FOUR of the following Coffman Conditions hold simultaneously:",
                    "1. Mutual Exclusion: At least one resource must be held in a non-shareable mode (only one process can use it at any instant).",
                    "2. Hold and Wait: A process must currently hold at least one resource and simultaneously request additional resources held by other processes.",
                    "3. No Preemption: Resources cannot be forcibly seized; a resource can only be released voluntarily by the process holding it after completing its task.",
                    "4. Circular Wait: A closed chain of processes {P0, P1, ..., Pn} exists such that P0 is waiting for a resource held by P1, P1 is waiting for P2, and Pn is waiting for a resource held by P0.",
                    "Deadlock Handling Approaches: Prevention (systematically invalidating at least one of the four Coffman conditions), Avoidance (using Dijkstra's Banker's Algorithm to verify that state transitions remain safe before granting requests), and Detection & Recovery (constructing Resource Allocation Graphs to detect cycles and terminating victim processes)."
                ]),
                ("2.6 Synchronization Primitives: Semaphores and Mutexes", [
                    "A Mutex is a locking mechanism used to synchronize access to a critical section, permitting only one thread of ownership at a time.",
                    "A Semaphore is a signaling integer variable S accessed via two atomic operations: wait() [decrement S, block if S <= 0] and signal() [increment S, unblock a waiting process]. Counting semaphores coordinate access to a finite pool of identical resource instances, while binary semaphores behave similarly to mutexes."
                ])
            ]
        )
    ]
    build_pdf("cs102_operating_systems.pdf", "CS102: Operating Systems Architecture & Resource Management", cs102_pages)

    # Document 3: Database Systems
    cs103_pages = [
        (
            "Relational Schema Normalization & ACID Guarantees",
            [
                ("3.1 Relational Database Normalization", [
                    "Normalization decomposes relations to minimize data redundancy and prevent insertion, update, and deletion anomalies:",
                    "• First Normal Form (1NF): All attributes contain atomic, indivisible values, and every tuple in the relation has a unique identifier (primary key).",
                    "• Second Normal Form (2NF): Relation is in 1NF and contains no partial functional dependencies (no non-prime attribute is functionally dependent on a proper subset of any candidate key).",
                    "• Third Normal Form (3NF): Relation is in 2NF and contains no transitive dependencies (for every functional dependency X -> Y, either X is a superkey or Y is a prime attribute).",
                    "• Boyce-Codd Normal Form (BCNF): A stricter variant of 3NF. A relation is in BCNF if and only if for every non-trivial functional dependency X -> Y, the determinant X is a candidate superkey."
                ]),
                ("3.2 ACID Transactional Properties", [
                    "A database transaction represents a logical unit of work that must satisfy the ACID criteria:",
                    "• Atomicity: All modifications performed by the transaction are successfully committed to the database, or the transaction is entirely aborted and rolled back ('all-or-nothing'). Enforced via Write-Ahead Logging (WAL) and undo logs.",
                    "• Consistency: A transaction transitions the database from one valid state to another valid state, preserving all integrity constraints, foreign keys, and business rules.",
                    "• Isolation: The execution of concurrent transactions produces the same state as if the transactions were executed sequentially without interference. Isolation prevents intermediate uncommitted changes from being visible to external transactions.",
                    "• Durability: Once a transaction commits, its effects persist permanently in non-volatile storage, even in the event of subsequent system crashes, power failures, or OS crashes. Enforced via redo logs."
                ])
            ]
        ),
        (
            "Concurrency Control, Isolation Levels & Transaction Anomalies",
            [
                ("3.3 Transaction Concurrency Anomalies", [
                    "Concurrent execution without proper isolation leads to classical data anomalies:",
                    "• Dirty Read: Transaction T1 updates a row without committing; Transaction T2 reads the uncommitted value; T1 aborts, leaving T2 with invalid phantom data.",
                    "• Non-Repeatable Read (Fuzzy Read): Transaction T1 reads a row; Transaction T2 modifies or deletes that row and commits; T1 re-reads the row and discovers that the values have changed.",
                    "• Phantom Read: Transaction T1 reads a set of rows satisfying a search predicate; Transaction T2 inserts or deletes rows matching that predicate and commits; T1 re-evaluates the query and discovers a differing set of rows."
                ]),
                ("3.4 ANSI SQL Isolation Levels", [
                    "Standard SQL defines four transaction isolation tiers offering trade-offs between concurrency and correctness:",
                    "1. Read Uncommitted: Allows Dirty Reads, Non-Repeatable Reads, and Phantom Reads. Lowest overhead.",
                    "2. Read Committed: Prevents Dirty Reads. Guarantees that any data read is committed at the moment of reading. Allows Non-Repeatable Reads and Phantom Reads (Default in PostgreSQL, Oracle, SQL Server).",
                    "3. Repeatable Read: Prevents Dirty Reads and Non-Repeatable Reads. Guarantees that rows read remain unchanged throughout the transaction. Phantom Reads may still occur (Default in MySQL InnoDB via Next-Key Locking).",
                    "4. Serializable: The strictest isolation level. Prevents all anomalies including Phantom Reads by simulating sequential execution via Two-Phase Locking (2PL) or Serializable Snapshot Isolation (SSI)."
                ])
            ]
        ),
        (
            "Storage Engines: B+ Trees, LSM-Trees & Hash Indexes",
            [
                ("3.5 B-Tree and B+ Tree Index Structures", [
                    "B+ Trees represent the ubiquitous standard index structure for relational storage engines (e.g. InnoDB, SQLite).",
                    "A B+ Tree is a self-balancing, m-way search tree where:",
                    "• All actual data records (or pointers to data tuples) reside exclusively in the leaf nodes.",
                    "• Leaf nodes are doubly linked sequentially, enabling highly efficient range queries (e.g., SELECT * WHERE id BETWEEN 100 AND 500) through sequential scanning.",
                    "• Internal nodes store solely routing keys and child pointers, providing high fan-out and shallow tree height (typically 3 to 4 levels for millions of records), requiring minimal disk I/O.",
                    "Search, insertion, and deletion complexity is guaranteed O(log n)."
                ]),
                ("3.6 Log-Structured Merge-Trees (LSM-Trees) vs Hash Indexes", [
                    "LSM-Trees are optimized for write-heavy database workloads (e.g. Cassandra, RocksDB). Writes are appended sequentially to an in-memory MemTable backed by a Write-Ahead Log (WAL). When full, the MemTable is flushed to disk as an immutable SSTable (Sorted String Table). Background compaction merges overlapping SSTables. LSM-Trees provide exceptional write throughput at the expense of higher read amplification.",
                    "Hash Indexes map keys to fixed slots using a cryptographic or non-cryptographic hash function. Hash indexes provide O(1) average-case point lookups (equality comparisons like WHERE id = 42), but cannot support range queries or partial prefix matches because hashes do not preserve lexical ordering."
                ])
            ]
        )
    ]
    build_pdf("cs103_database_acid_indexing.pdf", "CS103: Database Management Systems — Transactions & Storage", cs103_pages)

    # Document 4: Computer Networks
    cs104_pages = [
        (
            "Layered Architectures & Transport Protocols (TCP vs UDP)",
            [
                ("4.1 Layered Network Models: OSI 7-Layer vs TCP/IP 4-Layer", [
                    "Network architectures rely on layered abstractions to ensure modular protocol design:",
                    "• OSI 7-Layer Model: 7. Application, 6. Presentation, 5. Session, 4. Transport, 3. Network, 2. Data Link, 1. Physical.",
                    "• TCP/IP 4-Layer Model: 4. Application (HTTP, DNS, SMTP), 3. Transport (TCP, UDP), 2. Internet (IP, ICMP, ARP), 1. Link / Network Interface (Ethernet, Wi-Fi).",
                    "Encapsulation wraps headers at each descending layer: Application Data -> Transport Segment -> Network Packet/Datagram -> Link Frame -> Physical Bits."
                ]),
                ("4.2 Transport Layer Protocols: TCP versus UDP", [
                    "Transmission Control Protocol (TCP): Connection-oriented, full-duplex protocol providing reliable, ordered, and error-checked byte stream delivery between applications. Implements sliding-window flow control and dynamic congestion control. Header size ranges from 20 to 60 bytes.",
                    "User Datagram Protocol (UDP): Lightweight, connectionless transport protocol providing best-effort, unordered, and unreliable datagram transmission without flow or congestion control. UDP header is fixed at 8 bytes (Source Port, Destination Port, Length, Checksum). Ideal for latency-sensitive applications such as VoIP, online gaming, and DNS queries where packet loss is preferable to retransmission latency."
                ])
            ]
        ),
        (
            "TCP Connection Lifecycle, Flow Control & Congestion Management",
            [
                ("4.3 TCP 3-Way Handshake and 4-Way Termination", [
                    "To establish a reliable connection, TCP executes a Three-Way Handshake:",
                    "1. SYN: Client chooses an Initial Sequence Number (ISN) x and sends a segment with SYN flag set: SYN=1, Seq=x.",
                    "2. SYN-ACK: Server receives SYN, allocates buffers, selects ISN y, and responds: SYN=1, ACK=1, Seq=y, Ack=x+1.",
                    "3. ACK: Client acknowledges the server's sequence number: ACK=1, Seq=x+1, Ack=y+1. Connection transitions to ESTABLISHED.",
                    "Connection teardown uses a Four-Way Handshake:",
                    "1. Client sends FIN. 2. Server sends ACK. 3. Server finishes sending remaining data and transmits FIN. 4. Client replies with ACK and enters TIME_WAIT state (waiting 2 MSL - Maximum Segment Lifetime) before closing to ensure the final ACK was received."
                ]),
                ("4.4 Flow Control and Congestion Control", [
                    "Flow Control prevents a fast sender from overwhelming a slow receiver's buffer space. The receiver continuously advertises its available buffer capacity in the TCP header as the Receiver Window (rwnd). The sender guarantees that (LastByteSent - LastByteAcked) <= rwnd.",
                    "Congestion Control prevents senders from overwhelming intermediate network links and routers:",
                    "• Slow Start: Sender begins with Congestion Window cwnd = 1 MSS and doubles cwnd exponentially every round-trip time (RTT) until reaching the slow start threshold (ssthresh).",
                    "• Congestion Avoidance: Once cwnd >= ssthresh, cwnd increases linearly by 1 MSS per RTT (Additive Increase).",
                    "• Fast Retransmit and Fast Recovery: Upon receiving 3 duplicate ACKs, TCP retransmits the missing segment immediately without waiting for retransmission timer expiration, halves ssthresh, and resumes linear growth (Multiplicative Decrease - AIMD)."
                ])
            ]
        ),
        (
            "DNS Architecture, HTTP Evolution & TLS 1.3 Handshake",
            [
                ("4.5 Domain Name System (DNS) Resolution Hierarchy", [
                    "DNS provides a globally distributed, hierarchical database translating human-readable hostnames into IP addresses:",
                    "1. Root DNS Servers: Top of the hierarchy (13 root server IP clusters designated a.root-servers.net to m.root-servers.net).",
                    "2. Top-Level Domain (TLD) Servers: Manage specific top-level domains (.com, .org, .edu, .gov, country codes).",
                    "3. Authoritative Nameservers: Contain the definitive mapping records for an organization's domain.",
                    "Common DNS Record Types: A (maps hostname to IPv4 address), AAAA (maps hostname to IPv6 address), CNAME (canonical name alias), MX (mail exchange server), TXT (arbitrary text used for SPF/DKIM verification).",
                    "Recursive queries require the local DNS resolver to perform all external queries on behalf of the client, whereas iterative queries return referral addresses to the next server in the hierarchy."
                ]),
                ("4.6 HTTP Protocols and TLS 1.3 Security", [
                    "• HTTP/1.1: Introduced persistent connections (Keep-Alive), but suffered from Head-of-Line (HoL) blocking at the application layer.",
                    "• HTTP/2: Replaced text protocols with binary framing. Multiplexes multiple concurrent streams across a single TCP connection, eliminating application-level HoL blocking. Utilizes HPACK header compression.",
                    "• HTTP/3: Operates over QUIC (Quick UDP Internet Connections) using UDP as the transport layer. Solves TCP-level HoL blocking caused by packet loss and provides zero round-trip (0-RTT) connection resumption.",
                    "• TLS 1.3 Cryptographic Handshake: Modern security standard reducing handshake latency to 1 Round Trip Time (1-RTT). Eliminates insecure cipher suites and mandates ephemeral Diffie-Hellman key exchange (ECDHE) for forward secrecy."
                ])
            ]
        )
    ]
    build_pdf("cs104_computer_networks.pdf", "CS104: Computer Networks & Internet Protocol Architectures", cs104_pages)

    # Document 5: Python Concurrency
    cs105_pages = [
        (
            "CPython Internals, the Global Interpreter Lock & Process Models",
            [
                ("5.1 CPython Architecture and the Global Interpreter Lock (GIL)", [
                    "CPython (the reference implementation of Python) employs a Global Interpreter Lock (GIL). The GIL is a mutual-exclusion lock designed to prevent multiple native OS threads from executing Python bytecode simultaneously within a single Python process.",
                    "The primary historical justification for the GIL was simplifying memory management: CPython uses reference counting for garbage collection, which is not thread-safe without atomic operations or locking. By locking the interpreter, CPython avoids atomic reference-counting overhead.",
                    "Implications of the GIL:",
                    "• For CPU-bound tasks (e.g. matrix multiplication, image processing, cryptography), multi-threading in CPython provides NO performance gain and often degrades throughput due to context switching overhead and GIL lock contention.",
                    "• For I/O-bound tasks (e.g. network requests, database queries, file read/write), threads release the GIL while waiting for the OS system call to complete, allowing other threads to run concurrently."
                ]),
                ("5.2 Multithreading vs Multiprocessing in Python", [
                    "• threading Module: Manages native OS threads sharing a single virtual memory space and one CPython interpreter. Lightweight, low memory footprint. Highly effective for concurrent I/O operations.",
                    "• multiprocessing Module: Spawns independent operating system processes, each running its own CPython interpreter with an isolated memory space and private GIL. Bypasses the GIL entirely, achieving true parallel execution across multi-core CPUs for compute-intensive tasks.",
                    "Trade-offs: Processes require Inter-Process Communication (IPC) via Pipes or Queues and necessitate data serialization via pickle, incurring memory and serialization overhead."
                ])
            ]
        ),
        (
            "Asynchronous I/O, Asyncio Architecture & Coroutines",
            [
                ("5.3 Asyncio Event Loop Mechanics", [
                    "Asyncio implements single-threaded cooperative multitasking using an Event Loop.",
                    "The Event Loop is an infinite loop that monitors a set of I/O events, timers, and callbacks, multiplexing I/O using native OS primitives (epoll on Linux, kqueue on macOS, I/O Completion Ports [IOCP] on Windows).",
                    "• Coroutines: Declared using async def. When invoked, they return a coroutine object without executing immediately. Execution starts when awaited or scheduled on the event loop.",
                    "• The await keyword: Pauses execution of the current coroutine, yielding control back to the event loop so other tasks can execute until the awaited I/O operation finishes.",
                    "• asyncio.create_task(coro): Wraps a coroutine into an asyncio.Task and registers it immediately on the event loop for concurrent execution.",
                    "• asyncio.gather(*aws): Concurrently runs multiple awaitables and gathers their return values in ordered sequence."
                ]),
                ("5.4 Critical Pitfall: Blocking the Event Loop", [
                    "Because asyncio operates on a single OS thread, invoking synchronous blocking functions (e.g., time.sleep(), synchronous requests.get(), or heavy mathematical loops) blocks the entire event loop, preventing all other concurrent coroutines from progressing.",
                    "Mitigation Strategies: Use non-blocking async libraries (e.g. httpx, aiofiles, asyncpg), or offload blocking operations to a background thread using asyncio.to_thread(func, *args)."
                ])
            ]
        ),
        (
            "Synchronization Primitives, Thread Safety & Executors",
            [
                ("5.5 Thread Safety and Race Conditions", [
                    "Even with the GIL, Python code is NOT automatically thread-safe! The GIL guarantees atomicity only for single C-level bytecode instructions, not composite high-level Python operations.",
                    "Example: The statement `counter += 1` translates to three distinct bytecode instructions: LOAD_GLOBAL, INPLACE_ADD, and STORE_GLOBAL. If a thread context switch occurs between LOAD and STORE, race conditions occur, leading to silent data corruption.",
                    "Synchronization Primitives in threading and asyncio:",
                    "• Lock: Mutual exclusion lock with acquire() and release() methods, typically used via context manager `with lock:`.",
                    "• RLock (Reentrant Lock): A lock that can be acquired multiple times by the same thread without deadlocking.",
                    "• Semaphore: Limits concurrent access to a bounded pool of resources (e.g. limiting simultaneous HTTP client connections to 10).",
                    "• Event: Communicates state between threads or tasks; one thread signals `event.set()`, while other threads pause at `event.wait()` until notified."
                ]),
                ("5.6 High-Level Concurrent Futures: ThreadPoolExecutor & ProcessPoolExecutor", [
                    "The concurrent.futures module provides a high-level asynchronous execution framework:",
                    "• ThreadPoolExecutor: Thread pool for concurrent I/O operations, managing worker lifecycle automatically.",
                    "• ProcessPoolExecutor: Process pool for CPU-bound computations, distributing work across physical CPU cores without manual IPC management."
                ])
            ]
        )
    ]
    build_pdf("cs105_python_concurrency.pdf", "CS105: Python Concurrency, Asyncio & Parallel Programming", cs105_pages)
    print("All 5 course handouts generated successfully!")


if __name__ == "__main__":
    generate_all_documents()
