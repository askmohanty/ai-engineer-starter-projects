"""The RAG building blocks: load documents, chunk, embed, search, answer.

Projects 09 and 13 import this file, so it is kept small and dependency-light.
Chroma stores the vectors on disk in .chroma/ and uses its built-in embedding
model (all-MiniLM-L6-v2, downloaded on first use, runs locally for free).
"""

from pathlib import Path

import chromadb
from pypdf import PdfReader

from agentkit import run_agent

HERE = Path(__file__).parent
DOCS = HERE / "docs"
DB_PATH = HERE / ".chroma"
COLLECTION = "docs"


def load_documents(folder: Path = DOCS) -> dict[str, str]:
    documents = {}
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() in {".md", ".txt"}:
            documents[path.name] = path.read_text(encoding="utf-8")
        elif path.suffix.lower() == ".pdf":
            documents[path.name] = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return documents


def chunk(text: str, max_chars: int = 800, overlap: int = 1) -> list[str]:
    """Split on paragraphs, packing them into chunks of up to max_chars.

    `overlap` repeats the last N paragraphs of a chunk at the start of the next,
    so an answer that spans a boundary is still found.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], []
    for paragraph in paragraphs:
        if current and len("\n\n".join(current + [paragraph])) > max_chars:
            chunks.append("\n\n".join(current))
            current = current[-overlap:] if overlap else []
        current.append(paragraph)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def collection():
    return chromadb.PersistentClient(path=str(DB_PATH)).get_or_create_collection(COLLECTION)


def build_index(folder: Path = DOCS) -> int:
    client = chromadb.PersistentClient(path=str(DB_PATH))
    if COLLECTION in [c if isinstance(c, str) else c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    store = client.create_collection(COLLECTION)

    ids, texts, metadata = [], [], []
    for source, text in load_documents(folder).items():
        for n, piece in enumerate(chunk(text)):
            ids.append(f"{source}#{n}")
            texts.append(piece)
            metadata.append({"source": source, "chunk": n})
    store.add(ids=ids, documents=texts, metadatas=metadata)
    return len(ids)


def search(query: str, k: int = 4) -> list[dict]:
    result = collection().query(query_texts=[query], n_results=k)
    return [
        {"source": meta["source"], "text": text, "distance": round(distance, 3)}
        for text, meta, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])
    ]


SYSTEM = """Answer only from the numbered sources provided. Cite sources like [1].
If the sources do not contain the answer, say "I don't know from these documents."
Be concise and keep exact commands and numbers exactly as written."""


def answer(question: str, k: int = 4) -> tuple[str, list[dict]]:
    sources = search(question, k)
    context = "\n\n".join(f"[{n}] ({s['source']})\n{s['text']}" for n, s in enumerate(sources, 1))
    text, _ = run_agent(f"Sources:\n\n{context}\n\nQuestion: {question}", system=SYSTEM, verbose=False)
    return text, sources
