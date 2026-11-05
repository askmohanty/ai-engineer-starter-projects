"""Ask a question about the indexed documents.

    python 08-chat-with-docs-rag/ask.py "Payments are timing out, what should I check?"
    python 08-chat-with-docs-rag/ask.py --show-chunks "What does exit code 137 mean?"
"""

import sys

import rag

if __name__ == "__main__":
    args = sys.argv[1:]
    show_chunks = "--show-chunks" in args
    question = " ".join(a for a in args if a != "--show-chunks") or "Payments are timing out, what should I check?"

    text, sources = rag.answer(question)
    print(text, "\n")
    for n, s in enumerate(sources, 1):
        print(f"[{n}] {s['source']} (distance {s['distance']})")
        if show_chunks:
            print("    " + s["text"].replace("\n", "\n    ") + "\n")
