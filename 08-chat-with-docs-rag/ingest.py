"""Build the vector index from docs/ (Markdown, text and PDF files).

    python 08-chat-with-docs-rag/ingest.py
"""

import rag

if __name__ == "__main__":
    count = rag.build_index()
    print(f"Indexed {count} chunks from {rag.DOCS} into {rag.DB_PATH}")
