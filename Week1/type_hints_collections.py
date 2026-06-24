from typing import Optional, Union

name: str = "Vipul"
age: int = 22
score: float = 9.5
is_active: bool = True

# Function with type hints
def greet(name: str, times: int = 1) -> str:
    return f"Hello {name}! " * times

# Optional — value can be str OR None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Vipul", 2: "Alice"}
    return users.get(user_id)  # returns None if not found

# Union — accepts multiple types
def process(value: Union[str, int]) -> str:
    return str(value).upper()

# list and dict
def get_scores(names: list[str]) -> dict[str, int]:
    return {name: len(name) * 10 for name in names}

# tuple — fixed length, fixed types
def get_coords() -> tuple[float, float]:
    return (37.77, -122.41)

# nested types
def group_by_length(words: list[str]) -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    for word in words:
        key = len(word)
        if key not in result:
            result[key] = []
        result[key].append(word)
    return result

print(greet("Vipul", 3))
print(find_user(1))  
print(find_user(99))  
print(process(42))     
print(process("hi"))   

print(get_scores(["Vipul", "AI", "Engineer"]))


print(group_by_length(["cat", "dog", "mouse", "dolphin", "elephant", "ant", "bee"]))

from collections import defaultdict

# Without defaultdict — annoying boilerplate

"""
def group_normal(words: list[str]) -> dict[int, list[str]]:
    result = {}
    for word in words:
        key = len(word)
        if key not in result:      # have to check every time
            result[key] = []
        result[key].append(word)
    return result
"""

# With defaultdict — clean
def group_default(words: list[str]) -> dict[int, list[str]]:
    result: defaultdict[int, list[str]] = defaultdict(list)
    for word in words:
        result[len(word)].append(word)  # no check needed — list created automatically
    return dict(result)

# Real AI use case — group document chunks by source
chunks = [
    {"source": "doc1.pdf", "text": "chunk A"},
    {"source": "doc2.pdf", "text": "chunk B"},
    {"source": "doc1.pdf", "text": "chunk C"},
]

def group_by_source(chunks: list[dict]) -> dict[str, list[dict]]:
    grouped: defaultdict[str, list[dict]] = defaultdict(list)
    for chunk in chunks:
        grouped[chunk["source"]].append(chunk)
    return dict(grouped)

words = ["cat", "dog", "elephant", "ant", "bee", "tiger"]
print(group_default(words))

print(group_by_source(chunks))

from collections import Counter

# Count anything
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)

print(counts)                  
print(counts["apple"])           
print(counts["missing"])        
print(counts.most_common(2))     

# Real AI use case — track which tools an agent calls
tool_calls = ["web_search", "calculator", "web_search", "web_search", "summarizer", "calculator"]
usage = Counter(tool_calls)
print(usage.most_common())

# Count characters in a string
char_freq = Counter("hello world")
print(char_freq.most_common(3)) 

from typing import Optional
from collections import defaultdict, Counter, deque

def analyze_conversation(
    messages: list[dict[str, str]],
    window_size: int
) -> dict[str, Union[list, dict]]:
    """
    Analyze a conversation:
    - Keep a sliding window of recent messages
    - Count how often each role speaks
    - Group messages by role
    """
    window: deque[dict[str, str]]           = deque(maxlen=window_size)
    role_counts: Counter                     = Counter()
    by_role: defaultdict[str, list[str]]    = defaultdict(list)

    for msg in messages:
        window.append(msg)
        role_counts[msg["role"]] += 1
        by_role[msg["role"]].append(msg["content"])

    print(window)

    return {
        "recent_window": list(window),
        "role_counts":   dict(role_counts),
        "by_role":       dict(by_role),
    }


conversation = [
    {"role": "user",      "content": "What is Python?"},
    {"role": "assistant", "content": "A programming language."},
    {"role": "user",      "content": "What is FastAPI?"},
    {"role": "assistant", "content": "A web framework."},
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "Retrieval Augmented Generation."},
     {"role": "assistant", "content": "That's correct."},
]

result = analyze_conversation(conversation, window_size=6)
print("Recent:", [m["content"] for m in result["recent_window"]])
print("Counts:", result["role_counts"])