import os
import json
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY not found in environment. Running in offline/fallback mode.")

# -------------------------------------------------------------------------
# SUBJECT GROUP MAPPINGS FOR ROBUST FALLBACKS
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# MULTI-MODE FALLBACK DATA (MCQ, WRITTEN, CODING) FOR ALL 16 TOPICS
# -------------------------------------------------------------------------
FALLBACK_QUESTIONS = {
    'behavioral': {
        'easy': [
            {
                "type": "mcq",
                "question": "If you disagree with a team member about a technical approach, what is the best first step?",
                "options": {
                    "A": "Escalate the disagreement immediately to your engineering manager.",
                    "B": "Argue your point during the standup until they agree with you.",
                    "C": "Discuss the trade-offs privately with them, focusing on objective criteria.",
                    "D": "Implement your solution anyway and show them it works later."
                },
                "correct_answer": "C",
                "expected_answer": "Discussing trade-offs privately keeps conflicts constructive and focuses on technical merits rather than personal egos."
            },
            {
                "type": "written",
                "question": "Tell me about a time you had to learn a new tool or skill quickly. How did you handle it?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "STAR method response detailing context, learning resources, and outcomes."
            },
            {
                "type": "coding",
                "question": "Draft a professional email responding to a major system outage that affected external customers, explaining the issue and steps taken.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Clear, professional, empathetic, and action-oriented communication."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "A critical bug is discovered in production, and it is trace-backed to code written by a teammate. How do you respond?",
                "options": {
                    "A": "Publicly call them out in Slack so they fix it quickly.",
                    "B": "Focus on patching the system first, then run a blameless post-mortem.",
                    "C": "Tell management so they can review the teammate's performance.",
                    "D": "Ignore it since it is not your code."
                },
                "correct_answer": "B",
                "expected_answer": "Blameless post-mortems foster high trust and continuous improvements within engineering teams."
            },
            {
                "type": "written",
                "question": "Describe a time when you disagreed with a decision made by your manager. How did you present your perspective?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "STAR method response highlighting constructive feedback and alignment."
            },
            {
                "type": "coding",
                "question": "Describe in structured markdown a project timeline and resource plan for launching a feature that has a fixed, immovable deadline.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "A structured plan outlining priority levels, contingency buffers, and critical milestones."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What does a good engineering culture value most during technical debriefs or post-incident reviews?",
                "options": {
                    "A": "Identifying the single developer who made the mistake.",
                    "B": "Documenting system faults and creating actionable prevention tasks.",
                    "C": "Assigning blame to the QA testing department.",
                    "D": "Suppressing the incident report so external stakeholders do not worry."
                },
                "correct_answer": "B",
                "expected_answer": "Focusing on preventive actions and engineering redundancy rather than individual blame increases reliability."
            },
            {
                "type": "written",
                "question": "Tell me about a time when you had to take ownership of a long-term systemic failure in a team. What did you do to turn it around?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Demonstrating leadership, ownership, incremental progress, and structural changes."
            },
            {
                "type": "coding",
                "question": "Outline a comprehensive technical post-mortem report for a database crash that resulted in data loss for 5% of active users.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Detailed timeline, root cause analysis, mitigation steps, and permanent resolutions."
            }
        ]
    },
    'python': {
        'easy': [
            {
                "type": "mcq",
                "question": "What is the key difference between 'is' and '==' operators in Python?",
                "options": {
                    "A": "'is' compares values, '==' compares identities.",
                    "B": "'is' checks if two variables point to the same memory location, while '==' checks if their values are equal.",
                    "C": "They are completely identical and interchangeable.",
                    "D": "'is' is only used for strings, '==' is used for numbers."
                },
                "correct_answer": "B",
                "expected_answer": "'is' checks for object identity (same memory address), whereas '==' checks for value equality."
            },
            {
                "type": "written",
                "question": "Explain the difference between Python lists and tuples. When would you choose to use a tuple?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Lists are mutable, defined using `[]`. Tuples are immutable, defined using `()`. Use tuples for read-only data, dictionary keys, and faster iteration."
            },
            {
                "type": "coding",
                "question": "Write a Python function `remove_duplicates(lst)` that takes a list and returns a new list containing only unique elements, preserving their original order.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Use a set to track seen elements and list comprehension or loop to filter: `seen = set(); return [x for x in lst if not (x in seen or seen.add(x))]`."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "How does the Global Interpreter Lock (GIL) impact multi-threaded programs in Python?",
                "options": {
                    "A": "It speeds up CPU-bound operations in multi-threaded programs.",
                    "B": "It prevents multiple threads from downloading data concurrently in I/O-bound tasks.",
                    "C": "It restricts execution of Python bytecodes to a single CPU core at a time, limiting CPU-bound multi-threaded speedups.",
                    "D": "It prevents threads from writing to the same local variables."
                },
                "correct_answer": "C",
                "expected_answer": "The GIL ensures only one thread executes Python bytecodes at any time, meaning multi-threading does not speed up CPU-bound tasks in standard CPython."
            },
            {
                "type": "written",
                "question": "What are Python decorators? How do they work, and write a simple example.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Decorators are functions that take another function as an argument, extend its behavior without modifying it, and return a new function."
            },
            {
                "type": "coding",
                "question": "Write a Python generator function `fibonacci(n)` that yields the first n Fibonacci numbers.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Use a generator with `yield`: `a, b = 0, 1; for _ in range(n): yield a; a, b = b, a + b`."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "Which algorithm does Python use to determine Method Resolution Order (MRO) in multiple inheritance?",
                "options": {
                    "A": "Depth-First Search (DFS)",
                    "B": "C3 Linearization",
                    "C": "Kruskal's Algorithm",
                    "D": "Breadth-First Search (BFS)"
                },
                "correct_answer": "B",
                "expected_answer": "Python uses the C3 Linearization algorithm to compute the MRO, preserving local precedence and monotonicity."
            },
            {
                "type": "written",
                "question": "Explain Python's garbage collection mechanism. How does it handle reference cycles?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Python uses reference counting primarily. For reference cycles, it uses a generational cyclic garbage collector that periodically detects and cleans isolated cycles."
            },
            {
                "type": "coding",
                "question": "Write a Python class `Timer` implementing context manager methods (`__enter__` and `__exit__`) that measures and prints execution time of code inside its block.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Store start time in `__enter__` using `time.time()`, compute elapsed time in `__exit__` and print/log it."
            }
        ]
    },
    'system_design': {
        'easy': [
            {
                "type": "mcq",
                "question": "What is the primary purpose of a Content Delivery Network (CDN) in system design?",
                "options": {
                    "A": "To run heavy background database transactions.",
                    "B": "To cache and serve static assets close to users geographically, reducing latency.",
                    "C": "To compile application code.",
                    "D": "To monitor security logs of central servers."
                },
                "correct_answer": "B",
                "expected_answer": "CDNs cache files at edge locations closer to end users, reducing the load on origin servers and reducing latency."
            },
            {
                "type": "written",
                "question": "Explain the difference between SQL and NoSQL databases. When would you choose NoSQL?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "SQL databases are relational, schema-based, and support ACID. NoSQL are non-relational, flexible, and scale horizontally easily. Choose NoSQL for unstructured data or high throughput scale."
            },
            {
                "type": "coding",
                "question": "Write pseudo-code for a simple node lookup in a consistent hashing ring given a key hash and list of sorted node hashes.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Iterate through sorted node hashes to find the first hash >= key hash. If none matches, wrap around to the first node in the list."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "In the context of the CAP theorem, what does 'Partition Tolerance' mean?",
                "options": {
                    "A": "The system will automatically split files into sections.",
                    "B": "The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.",
                    "C": "Every node returns the identical write value instantly.",
                    "D": "The database database schema can be partitioned horizontally."
                },
                "correct_answer": "B",
                "expected_answer": "Partition tolerance means the system continues functioning even during network network splits/partitions between nodes."
            },
            {
                "type": "written",
                "question": "Explain the difference between horizontal scaling (scaling out) and vertical scaling (scaling up).",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Vertical scaling increases CPU/RAM of a single machine (hardware limit). Horizontal scaling adds more machines to the cluster (highly scalable, requires load balancing)."
            },
            {
                "type": "coding",
                "question": "Design a basic Token Bucket rate limiter in Python/pseudo-code. Implement an `allow_request(tokens)` function.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Maintain current token count and last refill timestamp. On request, refill tokens based on elapsed rate, then check if enough tokens exist."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the main benefit of using a Write-Back caching strategy over a Write-Through caching strategy?",
                "options": {
                    "A": "Write-Back ensures absolute data consistency in the database immediately.",
                    "B": "Write-Back reduces write latency by updating cache first and writing to database asynchronously.",
                    "C": "Write-Back is immune to data loss on sudden power failure.",
                    "D": "Write-Back simplifies cache invalidation mechanisms."
                },
                "correct_answer": "B",
                "expected_answer": "Write-Back writes to cache immediately and queue database updates, making write operations extremely fast."
            },
            {
                "type": "written",
                "question": "Describe how you would design a URL shortener service like Bitly. What are the key components and DB schema?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Use a Base62 encoding on unique IDs, relational/NoSQL key-value DB, redirect using HTTP 301/302, cache popular redirects with Redis, and scale horizontally using a Load Balancer."
            },
            {
                "type": "coding",
                "question": "Outline a high-level pseudo-code or configuration sequence for setting up an active-passive database failover system using health probes.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Ping active node. If probe fails 3 times, promote passive replica to primary master, rewrite DNS/IP redirect route, alert engineering."
            }
        ]
    },
    'data_structures': {
        'easy': [
            {
                "type": "mcq",
                "question": "What is the worst-case lookup time complexity in a standard Hash Table?",
                "options": {
                    "A": "O(1)",
                    "B": "O(log N)",
                    "C": "O(N)",
                    "D": "O(N^2)"
                },
                "correct_answer": "C",
                "expected_answer": "In the worst case (all keys collide into the same bucket), lookup becomes linear O(N)."
            },
            {
                "type": "written",
                "question": "Explain the difference between a Stack and a Queue. What are their primary operations?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Stack is LIFO (Last In First Out) using push/pop. Queue is FIFO (First In First Out) using enqueue/dequeue."
            },
            {
                "type": "coding",
                "question": "Write a function in Python `is_symmetric(root)` to check if a binary tree is a mirror of itself.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Implement helper `is_mirror(t1, t2)`: return True if both None, else check root values match and children are mirrors recursively."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "Which of the following data structures is typically used to implement Breadth-First Search (BFS) on a graph?",
                "options": {
                    "A": "Stack",
                    "B": "Queue",
                    "C": "Priority Queue",
                    "D": "Binary Search Tree"
                },
                "correct_answer": "B",
                "expected_answer": "BFS uses a Queue (FIFO) to explore nodes level-by-level, whereas DFS uses a Stack (LIFO)."
            },
            {
                "type": "written",
                "question": "What is a Binary Search Tree (BST)? What is its main property?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "A binary tree where the left child node's value is less than the parent's value, and the right child node's value is greater than the parent's value."
            },
            {
                "type": "coding",
                "question": "Write a Python function `has_cycle(head)` that detects if a singly linked list contains a cycle using Floyd's Cycle-Finding Algorithm.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Use slow and fast pointers. Move slow by 1 step and fast by 2 steps. If they meet, a cycle exists; if fast reaches end, no cycle."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the worst-case time complexity of building a binary heap from an unsorted array of N elements?",
                "options": {
                    "A": "O(N)",
                    "B": "O(N log N)",
                    "C": "O(log N)",
                    "D": "O(1)"
                },
                "correct_answer": "A",
                "expected_answer": "Using the bottom-up heapify method (Floyd's algorithm), building a heap takes O(N) time."
            },
            {
                "type": "written",
                "question": "Explain how a Red-Black Tree maintains self-balancing during insertions.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "RBT enforces properties: root/leaves are black, red node cannot have red children, same number of black nodes per path. Balance maintained via rotations and recoloring."
            },
            {
                "type": "coding",
                "question": "Write a Python function `lowest_common_ancestor(root, p, q)` that finds the lowest common ancestor node of two given nodes in a binary tree.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Recursively search left/right subtrees. If root matches p or q, return root. If both subtrees return non-None, root is LCA."
            }
        ]
    },
    'c_prog': {
        'easy': [
            {
                "type": "mcq",
                "question": "What does a pointer variable store in C?",
                "options": {
                    "A": "The value of another variable.",
                    "B": "The memory address of another variable.",
                    "C": "The binary code of the program.",
                    "D": "An integer array."
                },
                "correct_answer": "B",
                "expected_answer": "Pointers in C store memory addresses of variables."
            },
            {
                "type": "written",
                "question": "What is the difference between malloc() and calloc() in C?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "malloc() allocates uninitialized memory block. calloc() allocates multiple blocks and initializes them to zero."
            },
            {
                "type": "coding",
                "question": "Write a C function `void swap(int *x, int *y)` to swap the values of two integers using pointers.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`void swap(int *x, int *y) { int temp = *x; *x = *y; *y = temp; }`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is a memory leak in C?",
                "options": {
                    "A": "Accessing an array out of bounds.",
                    "B": "A compiler error when running low on system memory.",
                    "C": "Failing to free dynamically allocated heap memory after use.",
                    "D": "Overwriting stack pointer addresses."
                },
                "correct_answer": "C",
                "expected_answer": "Failing to call free() on memory allocated via malloc/calloc causes memory leaks."
            },
            {
                "type": "written",
                "question": "Explain pointer arithmetic in C. What happens when you add 1 to an integer pointer?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Adding 1 to a pointer increments its address by the size of the data type it points to (e.g., 4 bytes for int* on 32/64-bit systems)."
            },
            {
                "type": "coding",
                "question": "Write a C function `int str_len(char *s)` that returns the length of a string without using string.h.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`int str_len(char *s) { int len = 0; while(*s != '\\0') { len++; s++; } return len; }`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the primary function of the 'volatile' keyword in C?",
                "options": {
                    "A": "To prevent the compiler from optimizing reads/writes to the variable.",
                    "B": "To lock variables in multi-threaded code.",
                    "C": "To declare a variable whose type changes dynamically.",
                    "D": "To allocate memory in the read-only segment."
                },
                "correct_answer": "A",
                "expected_answer": "'volatile' tells the compiler that the value may change due to external factors (hardware, threads), preventing cache optimization."
            },
            {
                "type": "written",
                "question": "Explain the difference between stack and heap memory allocation in C.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Stack is managed automatically (LIFO, local variables, fast, small size). Heap is managed manually (malloc/free, slower, large size, persistent)."
            },
            {
                "type": "coding",
                "question": "Write a C recursive function `int count_nodes(void* root)` mockup logic or custom tree traversal to count nodes in a binary tree.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "If root node pointer is null return 0; else return 1 + recursive count of left child + recursive count of right child."
            }
        ]
    },
    'cpp_prog': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which C++ keyword is used to implement runtime polymorphism?",
                "options": {
                    "A": "template",
                    "B": "virtual",
                    "C": "static",
                    "D": "friend"
                },
                "correct_answer": "B",
                "expected_answer": "The 'virtual' keyword enables dynamic dispatch and runtime polymorphism."
            },
            {
                "type": "written",
                "question": "What is the key difference between a class and a struct in C++?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "In C++, classes default to private access/inheritance; structs default to public access/inheritance."
            },
            {
                "type": "coding",
                "question": "Create a simple C++ class `Rectangle` with private attributes `width` and `height`, and a public method `int getArea()`.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Class definition with constructor, private fields, and `getArea() { return width * height; }`."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What does std::move do in modern C++?",
                "options": {
                    "A": "It copies data to a new memory location.",
                    "B": "It deletes a pointer.",
                    "C": "It casts an lvalue to an rvalue reference to enable move semantics.",
                    "D": "It runs code asynchronously."
                },
                "correct_answer": "C",
                "expected_answer": "std::move converts an lvalue to an rvalue reference, prompting move constructors to take ownership instead of copying resources."
            },
            {
                "type": "written",
                "question": "Explain the concept of RAII (Resource Acquisition Is Initialization) in C++.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "RAII binds the lifecycle of resource ownership (locks, memory, files) to the lifetime of stack objects, releasing resources in destructors automatically."
            },
            {
                "type": "coding",
                "question": "Write a template function `T get_max(T a, T b)` in C++ that returns the maximum of two arguments.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`template <typename T> T get_max(T a, T b) { return (a > b) ? a : b; }`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is Virtual Inheritance used for in C++?",
                "options": {
                    "A": "To allow classes to inherit virtual functions.",
                    "B": "To solve the 'Diamond Problem' by ensuring only one subobject of a base class exists in multiple inheritance.",
                    "C": "To create abstract interface classes.",
                    "D": "To allocate base classes dynamically."
                },
                "correct_answer": "B",
                "expected_answer": "Virtual inheritance solves the diamond problem by merging base class instances in multiple inheritance trees."
            },
            {
                "type": "written",
                "question": "Explain smart pointers in C++ (unique_ptr, shared_ptr, weak_ptr) and how they prevent leaks.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "unique_ptr (exclusive ownership), shared_ptr (reference counting), weak_ptr (prevents circular references). They automatically call delete when references reach zero."
            },
            {
                "type": "coding",
                "question": "Implement a minimal custom smart pointer `CustomUniquePtr` in C++ that wraps a raw pointer and releases it in its destructor.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Template class with `T* ptr`, constructor, destructor running `delete ptr`, and overloaded `*` and `->` operators."
            }
        ]
    },
    'java_prog': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which Java keyword is used to make a class non-inheritable?",
                "options": {
                    "A": "static",
                    "B": "final",
                    "C": "abstract",
                    "D": "strictfp"
                },
                "correct_answer": "B",
                "expected_answer": "The 'final' keyword on a class prevents other classes from extending/inheriting it."
            },
            {
                "type": "written",
                "question": "Explain the difference between == and equals() in Java.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "== compares references (memory addresses). equals() compares object states (value equality)."
            },
            {
                "type": "coding",
                "question": "Write a Java method `boolean isDigitsOnly(String s)` that returns true if a string contains only digits.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Check for null/empty. Iterate characters and use `Character.isDigit(c)` or match regex `^[0-9]+$`."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is the effect of the 'volatile' keyword in Java multi-threading?",
                "options": {
                    "A": "It synchronized blocks of code from parallel execution.",
                    "B": "It forces thread scheduling priority.",
                    "C": "It ensures changes made to a variable by one thread are immediately visible to all other threads.",
                    "D": "It throws runtime thread conflicts."
                },
                "correct_answer": "C",
                "expected_answer": "volatile prevents caching of variables in threads, reading/writing directly to/from main memory."
            },
            {
                "type": "written",
                "question": "Explain JVM memory layout (Stack, Heap, Metaspace) and how garbage collection runs.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Stack stores frames/local variables. Heap stores object allocations. Metaspace stores class/method metadata. GC cleans unreferenced heap objects."
            },
            {
                "type": "coding",
                "question": "Write a thread-safe Singleton pattern in Java using Double-Checked Locking.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Private static volatile instance, private constructor, public method with synchronized block checking instance twice."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "How does Optimistic Locking differ from Pessimistic Locking in Java database transactions?",
                "options": {
                    "A": "Pessimistic locking relies on data version checking.",
                    "B": "Optimistic locking assumes conflicts are rare, checking versions before committing. Pessimistic locks database rows immediately.",
                    "C": "Optimistic locking is SQL only, Pessimistic is NoSQL only.",
                    "D": "Optimistic locking locks JVM memory blocks."
                },
                "correct_answer": "B",
                "expected_answer": "Optimistic locking uses a version field, failing only if version modified since read. Pessimistic locking locks records on read."
            },
            {
                "type": "written",
                "question": "Explain Java GC generations (Young, Old, Metaspace) and differences between Minor and Major GC.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Young gen holds short-lived objects (cleaned by Minor GC). Surviving objects move to Old gen (cleaned by Major/Full GC, which has higher latency)."
            },
            {
                "type": "coding",
                "question": "Design a basic Producer-Consumer thread-safe queue in Java using `wait()` and `notifyAll()`.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "LinkedList with limit. `produce()` waits while list is full, adds item, calls notifyAll. `consume()` waits while list is empty, pops, calls notifyAll."
            }
        ]
    },
    'web_dev': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which HTML tag is used to display an image with alternate text?",
                "options": {
                    "A": "<img src='url' alt='text'>",
                    "B": "<image href='url'>",
                    "C": "<pic source='url'>",
                    "D": "<figure src='url'>"
                },
                "correct_answer": "A",
                "expected_answer": "<img src='...'> is the standard HTML tag, using 'alt' for accessibility/alternative text."
            },
            {
                "type": "written",
                "question": "Explain the difference between HTTP GET and POST methods.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "GET requests data via URL parameters (cacheable, bookmarkable, limited size). POST submits data in body (secure, handles large payloads, modifies server state)."
            },
            {
                "type": "coding",
                "question": "Write a basic HTML form with fields for 'username', 'password', and a submit button, posting to '/login'.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`<form method='POST' action='/login'><input name='username'/><input type='password' name='password'/><button type='submit'>Submit</button></form>`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "Which CSS property is used to align flex container items along the main axis?",
                "options": {
                    "A": "align-items",
                    "B": "justify-content",
                    "C": "align-content",
                    "D": "flex-direction"
                },
                "correct_answer": "B",
                "expected_answer": "justify-content aligns elements along the main axis. align-items aligns them along the cross axis."
            },
            {
                "type": "written",
                "question": "What is CORS (Cross-Origin Resource Sharing)? Why does the browser enforce it?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "CORS is a security mechanism that allows or blocks resource requests between different domains, preventing malicious scripts on one site from accessing data on another."
            },
            {
                "type": "coding",
                "question": "Write a CSS rule to center a div horizontally and vertically inside a container of full viewport height.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Set container to: `display: flex; justify-content: center; align-items: center; min-height: 100vh;`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the difference between 'defer' and 'async' attributes in script tags?",
                "options": {
                    "A": "'defer' blocks HTML parsing, 'async' does not.",
                    "B": "'defer' scripts execute in order after HTML is fully parsed. 'async' scripts execute as soon as they download, potentially blocking parsing.",
                    "C": "They are exactly the same.",
                    "D": "'async' is for modules only."
                },
                "correct_answer": "B",
                "expected_answer": "'defer' executes scripts after HTML parse in order. 'async' executes immediately after download, interrupting parsing."
            },
            {
                "type": "written",
                "question": "Explain the Critical Rendering Path of a browser and how to optimize page rendering times.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Path: DOM -> CSSOM -> Render Tree -> Layout -> Paint. Optimize by minifying files, deferring non-critical scripts, and using CSS media queries."
            },
            {
                "type": "coding",
                "question": "Write a JavaScript function `debounce(fn, delay)` to debounce user input events (e.g. search suggestions).",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`function debounce(fn, delay) { let timer; return function(...args) { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); }; }`"
            }
        ]
    },
    'react_dev': {
        'easy': [
            {
                "type": "mcq",
                "question": "What React hook should you use to run code side-effects (e.g. data fetching)?",
                "options": {
                    "A": "useState",
                    "B": "useEffect",
                    "C": "useContext",
                    "D": "useReducer"
                },
                "correct_answer": "B",
                "expected_answer": "useEffect runs side-effects after the component renders in React functional components."
            },
            {
                "type": "written",
                "question": "What is the Virtual DOM? How does React update the real DOM?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "An in-memory lightweight representation of DOM. React diffs it against current DOM, batches changes, and updates only the differences (reconciliation)."
            },
            {
                "type": "coding",
                "question": "Write a React functional component `Counter` with a button that increments a displayed count value.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Functional component using `useState(0)` and button calling `setCount(prev => prev + 1)` on click."
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "Which hook caches a computed value to prevent recalculation on every render?",
                "options": {
                    "A": "useCallback",
                    "B": "useMemo",
                    "C": "useRef",
                    "D": "useEffect"
                },
                "correct_answer": "B",
                "expected_answer": "useMemo memoizes values. useCallback memoizes callbacks/function instances. useRef maintains mutable values."
            },
            {
                "type": "written",
                "question": "Explain state lift-up vs React Context API. When should you use Context?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Lifting state up shares state to adjacent parent/children. Context API shares state globally to avoid deep prop drilling (e.g. themes, user authentication)."
            },
            {
                "type": "coding",
                "question": "Write a custom React hook `useToggle(initialValue)` that returns a boolean state and a toggle function.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Hook returning `[val, () => setVal(v => !v)]` using `useState` internally."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What does the React 18 transition hook `useTransition` do?",
                "options": {
                    "A": "It adds css transition animations.",
                    "B": "It allows components to be loaded asynchronously.",
                    "C": "It marks state updates as non-blocking transitions, keeping the UI responsive during heavy renders.",
                    "D": "It handles route transitions."
                },
                "correct_answer": "C",
                "expected_answer": "useTransition splits state updates into high-priority updates (e.g. typing) and low-priority transitions (e.g. filtering list)."
            },
            {
                "type": "written",
                "question": "What is an Error Boundary in React? What lifecycles does it use?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Class components that catch JavaScript errors anywhere in child trees. They use `getDerivedStateFromError` to show fallback UI and `componentDidCatch` to log errors."
            },
            {
                "type": "coding",
                "question": "Write a basic class-based Error Boundary component in React showing a 'Something went wrong' heading on error.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Class component extending `React.Component` defining `state = { hasError: false }`, `getDerivedStateFromError() { return { hasError: true }; }` and standard `render()`."
            }
        ]
    },
    'dbms': {
        'easy': [
            {
                "type": "mcq",
                "question": "What does the 'I' in ACID transactions stand for?",
                "options": {
                    "A": "Integration",
                    "B": "Isolation",
                    "C": "Indexing",
                    "D": "Inheritance"
                },
                "correct_answer": "B",
                "expected_answer": "Isolation ensures concurrent transaction execution behaves identically to serial execution."
            },
            {
                "type": "written",
                "question": "What is a Primary Key and how does it differ from a Unique Key?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Primary key uniquely identifies rows and cannot contain NULL. Unique keys allow one or more NULL values (depending on database)."
            },
            {
                "type": "coding",
                "question": "Write SQL to create a table `users` with an auto-incrementing ID, username (varchar 50, unique), and date_created.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE, date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "Which Normal Form is violated if a table contains transitive dependencies?",
                "options": {
                    "A": "1NF",
                    "B": "2NF",
                    "C": "3NF",
                    "D": "BCNF"
                },
                "correct_answer": "C",
                "expected_answer": "3NF requires the table to be in 2NF and have no transitive dependencies (columns dependent on non-key columns)."
            },
            {
                "type": "written",
                "question": "Explain the difference between a clustered and a non-clustered index.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Clustered index stores rows physically in index order (1 per table). Non-clustered index stores index key with pointer to row data (multiple per table)."
            },
            {
                "type": "coding",
                "question": "Write an SQL query to retrieve the top 3 departments with the highest average salary from an `employees` table.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`SELECT department, AVG(salary) as avg_sal FROM employees GROUP BY department ORDER BY avg_sal DESC LIMIT 3;`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the primary purpose of the Write-Ahead Log (WAL) in database systems?",
                "options": {
                    "A": "To accelerate SELECT query times.",
                    "B": "To ensure durability and recovery by logging modifications before applying changes to database files.",
                    "C": "To enforce foreign key relationships.",
                    "D": "To archive old transaction histories."
                },
                "correct_answer": "B",
                "expected_answer": "WAL guarantees changes are recorded in non-volatile memory logs first, preventing data loss in crashes."
            },
            {
                "type": "written",
                "question": "Explain transaction Isolation Levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable).",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Read Uncommitted (allows dirty reads). Read Committed (prevents dirty reads). Repeatable Read (prevents non-repeatable reads). Serializable (complete lock isolation, prevents phantoms)."
            },
            {
                "type": "coding",
                "question": "Write a PostgreSQL transaction block that transfers $100 from account A to account B, checking for sufficient balance first.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "BEGIN; update accounts set balance = balance - 100 where id = 'A' and balance >= 100; update accounts set balance = balance + 100 where id = 'B'; COMMIT;"
            }
        ]
    },
    'sql_db': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which SQL clause is used to filter records returned by a GROUP BY group?",
                "options": {
                    "A": "WHERE",
                    "B": "HAVING",
                    "C": "ORDER BY",
                    "D": "LIMIT"
                },
                "correct_answer": "B",
                "expected_answer": "HAVING filters groups post-aggregation; WHERE filters individual rows pre-aggregation."
            },
            {
                "type": "written",
                "question": "What is the difference between DELETE and TRUNCATE SQL commands?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "DELETE is a DML statement (row-by-row, triggers run, transaction rollbacks allowed, WHERE clause supported). TRUNCATE is a DDL statement (fast, drops/re-creates table structure, locks page, cannot have WHERE)."
            },
            {
                "type": "coding",
                "question": "Write an SQL query to retrieve employee count grouped by department from an `employees` table.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department;`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is a SQL Common Table Expression (CTE)?",
                "options": {
                    "A": "A persistent database view.",
                    "B": "A temporary result set defined and referenced within a single SELECT/INSERT/UPDATE query.",
                    "C": "An indexing structure for search optimization.",
                    "D": "An access permission query."
                },
                "correct_answer": "B",
                "expected_answer": "CTEs are defined using the 'WITH' clause and exist temporarily for readability/modularity."
            },
            {
                "type": "written",
                "question": "Explain differences between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "INNER (matching in both). LEFT (all left rows, matching right). RIGHT (all right, matching left). FULL (all rows from both tables, filling NULLs where unmatched)."
            },
            {
                "type": "coding",
                "question": "Write a SQL query to find duplicate emails in a table `users` (Columns: id, email).",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`SELECT email FROM users GROUP BY email HAVING COUNT(email) > 1;`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "How does Database Partitioning differ from Database Sharding?",
                "options": {
                    "A": "Partitioning splits tables horizontally on one machine; Sharding splits data across multiple database machines.",
                    "B": "Partitioning is SQL-only; Sharding is NoSQL-only.",
                    "C": "Partitioning is for backups; Sharding is for speed.",
                    "D": "They are exactly the same concept."
                },
                "correct_answer": "A",
                "expected_answer": "Partitioning splits tables logically within a single DB instance. Sharding distributes tables across independent DB machines."
            },
            {
                "type": "written",
                "question": "Explain query optimization. How do indexes speed up queries, and what is EXPLAIN ANALYZE?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Indexes (B-Trees) limit table scans to log search. EXPLAIN shows query planner paths. ANALYZE runs it and outputs execution times and scan types."
            },
            {
                "type": "coding",
                "question": "Write a SQL query using window functions to find the rank of employees by salary in each department.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`SELECT id, name, department_id, salary, DENSE_RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) as rank FROM employees;`"
            }
        ]
    },
    'os': {
        'easy': [
            {
                "type": "mcq",
                "question": "What is the main task of the Operating System kernel?",
                "options": {
                    "A": "Rendering graphical desktop user interfaces.",
                    "B": "Managing hardware resources (memory, CPU, devices) and process scheduling.",
                    "C": "Compiling programming files.",
                    "D": "Handling internet web requests."
                },
                "correct_answer": "B",
                "expected_answer": "The kernel is the core of the OS, mediating access between user applications and the physical hardware."
            },
            {
                "type": "written",
                "question": "What is the difference between a process and a thread?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "A process is an isolated executing program instance with its own memory space. A thread is a lightweight execution unit inside a process sharing its memory space."
            },
            {
                "type": "coding",
                "question": "Write Python code mock structure to spawn a child process using `os.fork()`, printing 'Parent' in parent and 'Child' in child.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`pid = os.fork(); if pid == 0: print('Child') else: print('Parent')`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "Which process scheduling algorithm can result in infinite starvation of low-priority processes?",
                "options": {
                    "A": "Round Robin",
                    "B": "First-Come First-Served",
                    "C": "Priority Scheduling",
                    "D": "Shortest Remaining Time First"
                },
                "correct_answer": "C",
                "expected_answer": "Priority scheduling starvation occurs when high-priority tasks keep arriving. Mitigation is aging (raising priority of waiting tasks)."
            },
            {
                "type": "written",
                "question": "Explain virtual memory, paging, and what causes a page fault.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Virtual memory maps process addresses to physical RAM using pages. Page fault occurs when a process accesses a page not loaded in RAM, triggering OS to load it from disk."
            },
            {
                "type": "coding",
                "question": "Write a python snippet demonstrating synchronization between two threads accessing a shared variable using `threading.Lock()`.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Use lock as context manager: `lock = threading.Lock(); with lock: shared_counter += 1` to prevent race conditions."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is Thrashing in Operating Systems?",
                "options": {
                    "A": "Excessive swapping/paging activity where OS spends more time loading pages than executing work.",
                    "B": "A severe CPU hardware overheating shutdown.",
                    "C": "Process corruption from concurrent access.",
                    "D": "A memory allocation failure."
                },
                "correct_answer": "A",
                "expected_answer": "Thrashing occurs when the working set of active processes exceeds available physical memory, causing constant page swaps."
            },
            {
                "type": "written",
                "question": "What are the Coffman conditions required for deadlocks? How can we prevent them?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Prevent by ordering resources, requiring all acquisitions at once, or preemption."
            },
            {
                "type": "coding",
                "question": "Design in Python a thread-safe Queue class using Condition variables to coordinate producer-consumer flows.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Maintain list, `Condition` object. `put()` locks condition, waits while queue full, appends, notifies. `get()` waits while empty, pops, notifies."
            }
        ]
    },
    'networks': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which OSI model layer handles IP routing and forwarding?",
                "options": {
                    "A": "Physical Layer",
                    "B": "Data Link Layer",
                    "C": "Network Layer",
                    "D": "Transport Layer"
                },
                "correct_answer": "C",
                "expected_answer": "The Network Layer is responsible for addressing, routing, and switching packets across networks."
            },
            {
                "type": "written",
                "question": "Explain TCP vs UDP protocols. When would you use UDP?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "TCP is connection-oriented, reliable, orders packets, flows control. UDP is connectionless, unreliable, fast, no overhead. Use UDP for streaming, gaming, DNS."
            },
            {
                "type": "coding",
                "question": "Write a Python script to resolve a hostname (e.g. 'google.com') to an IP address.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`import socket; print(socket.gethostbyname('google.com'))`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is the purpose of the 3-Way Handshake in TCP?",
                "options": {
                    "A": "To compress incoming headers.",
                    "B": "To synchronize sequence numbers (SYN/ACK) and establish a reliable socket connection.",
                    "C": "To authenticate SSL/TLS certs.",
                    "D": "To scan open network ports."
                },
                "correct_answer": "B",
                "expected_answer": "Handshake (SYN -> SYN-ACK -> ACK) initializes sequence tracking on both ends to ensure reliability."
            },
            {
                "type": "written",
                "question": "Explain how Domain Name System (DNS) works. Discuss Recursive vs Iterative resolution.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Resolves domain to IP. Resolver asks Root, TLD, and Authoritative servers. Recursive resolvers do the entire lookup chain. Iterative returns best known reference."
            },
            {
                "type": "coding",
                "question": "Write a Python TCP client that connects to '127.0.0.1' on port 8080 and sends a message.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Create socket: `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('127.0.0.1', 8080)); s.sendall(b'Hello'); s.close();`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the main task of Border Gateway Protocol (BGP) on the Internet?",
                "options": {
                    "A": "Assigning IP addresses dynamically to clients.",
                    "B": "Routing packets within a local area network (LAN).",
                    "C": "Exchanging routing paths and reachability information between Autonomous Systems (AS) on the web.",
                    "D": "Encrypting network card packets."
                },
                "correct_answer": "C",
                "expected_answer": "BGP is the routing protocol of the global Internet, routing packets between autonomous systems."
            },
            {
                "type": "written",
                "question": "Describe in detail all steps that occur when a user types 'https://google.com' and hits Enter in their browser.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "DNS resolution, TCP 3-way handshake, TLS handshake (negotiate keys/certs), HTTP GET request, Server processes and sends response, Browser renders DOM/CSSOM."
            },
            {
                "type": "coding",
                "question": "Write a simple multi-threaded TCP echo server in Python listening on port 8080 that spawns a thread for each incoming connection.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`bind` and `listen` socket. Loop running `conn, addr = s.accept()`, then spawn a `threading.Thread(target=handle_client, args=(conn,)).start()`."
            }
        ]
    },
    'cybersecurity': {
        'easy': [
            {
                "type": "mcq",
                "question": "What does HTTPS add to standard HTTP to make it secure?",
                "options": {
                    "A": "Database triggers.",
                    "B": "SSL/TLS encryption for data in transit.",
                    "C": "Two-factor client logins.",
                    "D": "Cookie session timeouts."
                },
                "correct_answer": "B",
                "expected_answer": "HTTPS layers HTTP over SSL/TLS protocols to encrypt communication and authenticate server identity."
            },
            {
                "type": "written",
                "question": "What is SQL Injection? How can developers prevent it?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "SQL Injection occurs when untrusted user inputs are directly concatenated into SQL queries. Prevent by using parameterized queries/prepared statements."
            },
            {
                "type": "coding",
                "question": "Write a Python function `hash_password(password)` that uses hashlib to securely hash a password using SHA-256 with a salt.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`salt = os.urandom(16); return salt + hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What vulnerability occurs when user input is rendered directly in a web page without HTML escaping?",
                "options": {
                    "A": "SQL Injection",
                    "B": "Buffer Overflow",
                    "C": "Cross-Site Scripting (XSS)",
                    "D": "Man-in-the-Middle Attack"
                },
                "correct_answer": "C",
                "expected_answer": "XSS allows attackers to inject malicious scripts into trusted websites, executing code in other users' browsers."
            },
            {
                "type": "written",
                "question": "Explain asymmetric (public-key) vs symmetric cryptography.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Symmetric uses the same key for encryption/decryption (fast, needs secure key exchange). Asymmetric uses a public key (encrypt) and private key (decrypt) (slower, secure key exchange)."
            },
            {
                "type": "coding",
                "question": "Write a Python function `is_strong_password(p)` checking if password length is >= 8, has >= 1 uppercase, >= 1 lowercase, and >= 1 digit.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Validate password checks: `return len(p) >= 8 and any(c.isupper() for c in p) and any(c.islower() for c in p) and any(c.isdigit() for c in p)`."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "How does a anti-CSRF token protect web applications against Cross-Site Request Forgery?",
                "options": {
                    "A": "It encrypts the entire cookie storage.",
                    "B": "It validates that request originates from user's physical IP address.",
                    "C": "It is a unique, secret value embedded in forms that verifies the request came from the app's verified interface, not a third-party script.",
                    "D": "It forces users to enter a CAPTCHA."
                },
                "correct_answer": "C",
                "expected_answer": "CSRF tokens ensure that requests originate from within the authenticated user session context rather than malicious cross-site forms."
            },
            {
                "type": "written",
                "question": "Describe the OAuth 2.0 Authorization Code flow and how it protects user credentials.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Client redirects user to Auth server. User authenticates and grants permission. Auth server redirects with auth code. Client exchanges code for access token via backend. Avoids exposure of user passwords to client app."
            },
            {
                "type": "coding",
                "question": "Write a Python function demonstrating decryption of an AES ciphertext using a given key and IV with the cryptography library.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Using cryptography.hazmat: create Cipher with AES(key) and CBC(iv), create decryptor, decrypt ciphertext, unpad result."
            }
        ]
    },
    'cloud_devops': {
        'easy': [
            {
                "type": "mcq",
                "question": "What is the primary benefit of using containers (like Docker) over traditional VMs?",
                "options": {
                    "A": "Containers include their own complete guest OS kernel.",
                    "B": "Containers share the host OS kernel, making them lightweight, fast to boot, and resource-efficient.",
                    "C": "Containers are SQL-only.",
                    "D": "Containers are immune to network lag."
                },
                "correct_answer": "B",
                "expected_answer": "Containers package apps with dependencies but share the host kernel, avoiding the overhead of separate VM hypervisors."
            },
            {
                "type": "written",
                "question": "What is CI/CD? Discuss its core phases.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "CI (Continuous Integration: commit, build, test code). CD (Continuous Delivery/Deployment: automatically release build outputs to staging/production)."
            },
            {
                "type": "coding",
                "question": "Write a simple Dockerfile for a Python script `main.py` using `python:3.11-slim` base image.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`FROM python:3.11-slim; WORKDIR /app; COPY main.py .; CMD [\"python\", \"main.py\"]`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is the main role of Kubernetes in devops environments?",
                "options": {
                    "A": "To compile and package code packages.",
                    "B": "To write database schemas.",
                    "C": "To orchestrate, scale, schedule, and manage containerized applications across a cluster.",
                    "D": "To monitor network firewalls."
                },
                "correct_answer": "C",
                "expected_answer": "Kubernetes automated container deployment, scaling, load balancing, self-healing, and rollout/rollbacks."
            },
            {
                "type": "written",
                "question": "What is Infrastructure as Code (IaC)? What are its advantages?",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Managing/provisioning infrastructure (VMs, networks) via declarative configuration files (e.g. Terraform, CloudFormation). Advantages: speed, consistency, version control."
            },
            {
                "type": "coding",
                "question": "Write a basic GitHub Actions workflow YAML block that runs on push to `main` branch, checkout code, and runs a test script.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`on: push: branches: [main] ... steps: - uses: actions/checkout@v3 - run: python -m unittest`"
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "How does Blue-Green deployment differ from Canary deployment?",
                "options": {
                    "A": "Blue-Green keeps two identical environments (active/idle) and switches DNS; Canary rolls updates incrementally to a subset of users first.",
                    "B": "Blue-Green is SQL-only, Canary is NoSQL-only.",
                    "C": "Canary deployment is slower and less safe.",
                    "D": "Blue-Green deployment does not support rollback."
                },
                "correct_answer": "A",
                "expected_answer": "Blue-Green switches traffic fully between two production environments. Canary introduces code progressively to users to test stability."
            },
            {
                "type": "written",
                "question": "Explain the architectural differences between Serverless (FaaS) and standard Cloud Instances (IaaS).",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "FaaS runs functions on demand (scales to zero, charged per execution millisecond, stateless, managed runtime). IaaS runs virtual machines (continuously billed, stateful, user manages OS)."
            },
            {
                "type": "coding",
                "question": "Write a minimal Terraform configuration blocks declaring an AWS provider and launching an EC2 instance resource.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`provider \"aws\" { region = \"us-east-1\" } resource \"aws_instance\" \"web\" { ami = \"ami-12345\" instance_type = \"t2.micro\" }`"
            }
        ]
    },
    'sys_prog': {
        'easy': [
            {
                "type": "mcq",
                "question": "Which system call is used to create a new child process in Unix systems?",
                "options": {
                    "A": "exec()",
                    "B": "fork()",
                    "C": "wait()",
                    "D": "pipe()"
                },
                "correct_answer": "B",
                "expected_answer": "fork() duplicates the calling process to create a child process."
            },
            {
                "type": "written",
                "question": "Explain User Space vs Kernel Space in operating systems.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "User space is restricted memory where user apps execute. Kernel space has complete, privileged access to memory and physical hardware."
            },
            {
                "type": "coding",
                "question": "Write a C code snippet to open a file 'log.txt' for writing, write 'LOG' to it, and close the file descriptor.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "`int fd = open(\"log.txt\", O_WRONLY|O_CREAT, 0644); write(fd, \"LOG\", 3); close(fd);`"
            }
        ],
        'medium': [
            {
                "type": "mcq",
                "question": "What is a Signal in operating systems?",
                "options": {
                    "A": "A physical interrupt on the motherboard.",
                    "B": "An asynchronous notification sent to a process to notify it of a system/hardware event.",
                    "C": "A database synchronization flag.",
                    "D": "A thread variable."
                },
                "correct_answer": "B",
                "expected_answer": "Signals (like SIGINT, SIGKILL, SIGSEGV) notify processes of OS events or termination requests."
            },
            {
                "type": "written",
                "question": "Explain static compilation vs dynamic compilation and loading.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Static compiles libraries into final executable binary (large binary size, independent). Dynamic links libraries at runtime (.so/.dll files) (smaller size, needs shared libs on system)."
            },
            {
                "type": "coding",
                "question": "Write a C program that catches SIGINT (Ctrl+C), prints a message, and clean exits.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Define signal handler `void handle(int sig) { print; exit(0); }`. Register inside main using `signal(SIGINT, handle)`."
            }
        ],
        'hard': [
            {
                "type": "mcq",
                "question": "What is the difference between a named pipe (FIFO) and a socket in Unix IPC?",
                "options": {
                    "A": "Pipes are restricted to unidirectional communication on the local system; sockets support bidirectional local/network communication.",
                    "B": "Pipes are SQL-only, Sockets are network-only.",
                    "C": "Sockets do not support concurrent streams.",
                    "D": "They are identical."
                },
                "correct_answer": "A",
                "expected_answer": "FIFOs are files supporting unidirectional local byte streams. Sockets support bi-directional streams locally (Unix sockets) or across networks (TCP/UDP)."
            },
            {
                "type": "written",
                "question": "Explain how ELF format, dynamic linkers, and LD_PRELOAD intercept function calls in Linux.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "ELF specifies sections. Dynamic linker (ld.so) resolves undefined symbols in GOT/PLT. LD_PRELOAD loads specified libs first, overriding standard symbols."
            },
            {
                "type": "coding",
                "question": "Write C code to create a pipe, fork, and redirect parent's stdout to child's stdin using `pipe()` and `dup2()`.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "expected_answer": "Call `pipe(fd)`. Fork. In parent: `dup2(fd[1], STDOUT_FILENO); close;`. In child: `dup2(fd[0], STDIN_FILENO); close;`."
            }
        ]
    }
}

def get_fallback_questions(topic, difficulty, mode):
    """Retrieve fallback questions matching the topic, difficulty, and mode."""
    # Find matching topic in FALLBACK_QUESTIONS
    group_data = FALLBACK_QUESTIONS.get(topic)
    if not group_data:
        # Fallback to python if not found
        group_data = FALLBACK_QUESTIONS.get('python', FALLBACK_QUESTIONS['behavioral'])
        
    # Get questions for difficulty
    difficulty_pool = group_data.get(difficulty)
    if not difficulty_pool:
        difficulty_pool = group_data.get('medium')
        
    # Filter by mode (if 'mixed', return a subset of available types)
    if mode == 'mixed':
        mixed_list = []
        
        # Load elements from easy/medium/hard to make a diverse mix
        q_pool = []
        for diff in ['easy', 'medium', 'hard']:
            if diff in group_data:
                q_pool.extend(group_data[diff])
            
        mcq_qs = [q for q in q_pool if q['type'] == 'mcq']
        written_qs = [q for q in q_pool if q['type'] == 'written']
        coding_qs = [q for q in q_pool if q['type'] == 'coding']
        
        # Pull enough questions
        if mcq_qs: mixed_list.append(mcq_qs[0])
        if written_qs: mixed_list.append(written_qs[0])
        if coding_qs: mixed_list.append(coding_qs[0])
        if len(mcq_qs) > 1: mixed_list.append(mcq_qs[1])
        if len(written_qs) > 1: mixed_list.append(written_qs[1])
        
        # Padding if needed
        while len(mixed_list) < 5:
            mixed_list.append(q_pool[len(mixed_list) % len(q_pool)])
            
        return mixed_list[:5]
        
    else:
        # Extract questions of this specific mode
        q_pool = []
        for diff in ['easy', 'medium', 'hard']:
            if diff in group_data:
                q_pool.extend(group_data[diff])
            
        typed_qs = [q for q in q_pool if q['type'] == mode]
        
        # Ensure we have at least 5 questions (can duplicate if pool is small)
        while len(typed_qs) < 5:
            typed_qs.extend(typed_qs or q_pool)
            
        return typed_qs[:5]

def get_fallback_evaluation(question_text, user_answer):
    """Generate a realistic, constructive evaluation if the API fails."""
    word_count = len(user_answer.split()) if user_answer else 0
    
    if word_count < 10:
        score = 2
        strengths = "* Brief response provided."
        weaknesses = "* The answer is extremely short or blank.\n* Lacks structure, examples, or technical detail."
        improved_answer = "A high-quality answer would expand on the core terms. For example, if asked about lists and tuples: 'Python lists are mutable, meaning their elements can be modified after creation, and are defined using square brackets `[]`. Tuples are immutable sequence types, meaning their elements cannot be changed, defined with parentheses `()`. In production environments, tuples are faster and protect data integrity.'"
        tips = "* Always structure your answer using the STAR method (Situation, Task, Action, Result) for behavioral questions, or define terms, explain differences, and provide code examples for technical questions.\n* Try to aim for at least 3-4 sentences in your answer."
    elif word_count < 40:
        score = 5
        strengths = "* Identified key terms related to the question.\n* Straightforward explanation."
        weaknesses = "* Lacks depth and specific examples.\n* Could benefit from structured formatting (bullet points, code blocks where applicable)."
        improved_answer = f"Here is a comprehensive answer:\n\nWhen answering '{question_text}', it is best to provide concrete examples or explain the underlying mechanics. For technical questions, discuss memory, performance, or use-cases. For behavioral, outline the context, your action, and the positive business impact."
        tips = "* Elaborate further on the 'why' behind your points.\n* Use formatting to make the answer easy to read.\n* Provide a quick, realistic code snippet or case study to demonstrate expertise."
    else:
        score = 8
        strengths = "* Detailed and thoughtful answer.\n* Good coverage of key concepts.\n* Clear structure and professional tone."
        weaknesses = "* Could provide slightly more technical depth or explicitly highlight edge cases.\n* Could reference real-world system constraints or architectural alternatives."
        improved_answer = "This is a solid response! To make it a 10/10, consider integrating a concise real-world scenario where you applied this knowledge, or highlight the performance implications (e.g., O(1) lookup speeds vs O(N) linear scans, or business metric improvements)."
        tips = "* You are doing great! Keep structure clean.\n* Ensure you mention metrics and performance considerations where relevant."

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improved_answer": improved_answer,
        "tips": tips
    }

# -------------------------------------------------------------------------
# GEMINI API WRAPPERS
# -------------------------------------------------------------------------

def generate_session_questions(topic, difficulty, mode):
    """
    Generate 5 tailored questions using the Gemini API.
    If the API key is not set, or an exception occurs, falls back to pre-defined questions.
    """
    if not os.getenv("GEMINI_API_KEY"):
        logger.info("No Gemini API key. Using fallback questions.")
        return get_fallback_questions(topic, difficulty, mode)

    topic_labels = {
        'behavioral': 'Behavioral / Leadership Questions',
        'python': 'Python & Django Software Development',
        'system_design': 'System Design & Scalability',
        'data_structures': 'Data Structures & Algorithms',
        'c_prog': 'C Programming & Pointers',
        'cpp_prog': 'C++ OOP & STL Library',
        'java_prog': 'Java JVM & Concurrency',
        'web_dev': 'Web Development (Full Stack Basics)',
        'react_dev': 'React Development & Virtual DOM',
        'dbms': 'Database Management Systems',
        'sql_db': 'Relational Database Queries & Schema Design',
        'os': 'Operating Systems Kernels & Memory Management',
        'networks': 'Computer Networks & Network Protocols',
        'cybersecurity': 'Cyber Security Concepts & Vulnerabilities',
        'cloud_devops': 'Cloud & DevOps Containers & Deployment',
        'sys_prog': 'System Programming Compiling & Execution Layout'
    }
    topic_desc = topic_labels.get(topic, topic)
    
    prompt = f"""
    Generate exactly 5 realistic, highly professional, and challenging interview questions for a candidate.
    Topic: {topic_desc}
    Difficulty level: {difficulty}
    Target Assessment Mode: {mode} (mixed, mcq, written, or coding)

    You must return a JSON array containing exactly 5 question objects.
    Each object in the array must strictly have these keys:
    - "type": "mcq" | "written" | "coding"
    - "question": "Question text or coding problem statement"
    - "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}} (populate strings if type is "mcq", otherwise leave options empty strings like "")
    - "correct_answer": "A" | "B" | "C" | "D" (populate if type is "mcq", otherwise leave empty string "")
    - "expected_answer": "Brief explanation or expected solution snippet"

    In "mixed" mode, generate a combination of MCQs, written, and coding questions.
    In "mcq" mode, all 5 questions must be "mcq".
    In "written" mode, all 5 questions must be "written".
    In "coding" mode, all 5 questions must be "coding" (coding problems where code is written in a text box).

    Do not include markdown tags like ```json or ```. Just return the raw JSON array string.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse output
        raw_text = response.text.strip()
        # Clean potential markdown wrappers if the model ignored request
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json"):
                raw_text = "\n".join(lines[1:-1])
            elif lines[0].startswith("```"):
                raw_text = "\n".join(lines[1:-1])
        
        questions = json.loads(raw_text)
        if isinstance(questions, list) and len(questions) >= 5:
            # Validate properties
            valid_questions = []
            for q in questions[:5]:
                # Standardize structures
                opts = q.get("options", {})
                valid_questions.append({
                    "type": q.get("type", "written"),
                    "question": q.get("question", ""),
                    "option_a": opts.get("A", "") if isinstance(opts, dict) else "",
                    "option_b": opts.get("B", "") if isinstance(opts, dict) else "",
                    "option_c": opts.get("C", "") if isinstance(opts, dict) else "",
                    "option_d": opts.get("D", "") if isinstance(opts, dict) else "",
                    "correct_answer": q.get("correct_answer", ""),
                    "expected_answer": q.get("expected_answer", "")
                })
            return valid_questions
        else:
            raise ValueError("Invalid format returned by Gemini API")
            
    except Exception as e:
        logger.error(f"Error calling Gemini API for questions: {e}. Falling back.")
        fallback_qs = get_fallback_questions(topic, difficulty, mode)
        # Convert fallback format
        valid_fallback = []
        for q in fallback_qs:
            opts = q.get("options", {})
            valid_fallback.append({
                "type": q.get("type", "written"),
                "question": q.get("question", ""),
                "option_a": opts.get("A", ""),
                "option_b": opts.get("B", ""),
                "option_c": opts.get("C", ""),
                "option_d": opts.get("D", ""),
                "correct_answer": q.get("correct_answer", ""),
                "expected_answer": q.get("expected_answer", "")
            })
        return valid_fallback


def evaluate_candidate_answer(question_text, user_answer, question_type="written"):
    """
    Evaluate candidate's answer using the Gemini API.
    Adapts prompt context based on whether the question is coding or standard written response.
    Returns a structured dictionary with keys: score (int), strengths (str), weaknesses (str),
    improved_answer (str), and tips (str).
    """
    if not os.getenv("GEMINI_API_KEY"):
        logger.info("No Gemini API key. Using fallback evaluator.")
        return get_fallback_evaluation(question_text, user_answer)

    # Customize prompt based on type
    if question_type == "coding":
        prompt_type_guidelines = """
        This is a coding interview question.
        Please evaluate the candidate's code response. Inspect:
        - Logic correctness and algorithm flow.
        - Code quality and edge cases.
        - Complexity awareness (Big O time/space complexity).

        In the JSON response, map the keys as follows:
        - "strengths": A markdown-formatted explanation of the candidate's "Correct Approach" (what they got right, their time/space complexity analysis).
        - "weaknesses": A markdown-formatted list of "Mistakes Identified" (bugs, bad practices, sub-optimal paths).
        - "improved_answer": A markdown-formatted "Optimized Solution" in the candidate's target language (syntactically correct, commented code block with complexity analysis).
        - "tips": Actionable feedback on improving algorithm designs or memory structures.
        """
    else:
        prompt_type_guidelines = """
        This is a written technical/behavioral interview question.
        Please evaluate the candidate's response. Inspect terminology correctness, conceptual clarity, and completeness.

        In the JSON response, map the keys as follows:
        - "strengths": A markdown-formatted list of key strengths.
        - "weaknesses": A markdown-formatted list of weaknesses or missing elements.
        - "improved_answer": A model 10/10 comprehensive response.
        - "tips": Actionable tips for future preparation.
        """

    prompt = f"""
    You are an expert technical interviewer. Grade the candidate's response.

    Question:
    {question_text}

    Candidate's Answer:
    {user_answer or "[No answer provided]"}

    {prompt_type_guidelines}

    You must evaluate the response and return a JSON object with the following keys:
    - "score": An integer between 0 and 10 representing the grade.
    - "strengths": String.
    - "weaknesses": String.
    - "improved_answer": String.
    - "tips": String.

    Ensure that the response is strictly a valid JSON object. Do not wrap it in markdown block tags like ```json.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        raw_text = response.text.strip()
        # Clean potential markdown wrappers
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json"):
                raw_text = "\n".join(lines[1:-1])
            elif lines[0].startswith("```"):
                raw_text = "\n".join(lines[1:-1])
                
        evaluation = json.loads(raw_text)
        
        # Sanitize and ensure format compliance
        score = evaluation.get("score", 5)
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = 5
            
        return {
            "score": score,
            "strengths": evaluation.get("strengths", "Good try."),
            "weaknesses": evaluation.get("weaknesses", "Could be expanded."),
            "improved_answer": evaluation.get("improved_answer", "N/A"),
            "tips": evaluation.get("tips", "Practice makes perfect.")
        }
        
    except Exception as e:
        logger.error(f"Error calling Gemini API for evaluation: {e}. Falling back.")
        return get_fallback_evaluation(question_text, user_answer)
