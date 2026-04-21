import argparse
from pathlib import Path

from .config import CORPUS_DIR
from .index import build_index, save_index
from .rag import RAGSystem


def build_command() -> None:
    index, metadata = build_index(CORPUS_DIR)
    save_index(index, metadata)
    print(f"Built index from {len(metadata)} chunks.")


def ask_command(question: str) -> None:
    rag = RAGSystem()
    answer, contexts = rag.generate(question)

    print("\nAnswer:\n")
    print(answer)
    print("\nRetrieved contexts:\n")
    for i, ctx in enumerate(contexts, start=1):
        print(f"{i}. {ctx['source']} (chunk {ctx['chunk_id']}, score={ctx['score']:.4f})")
        print(ctx["text"])
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Amharic RAG assistant")
    parser.add_argument("--build", action="store_true", help="Build the FAISS index")
    parser.add_argument("--ask", type=str, help="Ask a question in Amharic")

    args = parser.parse_args()

    if args.build:
        build_command()
    elif args.ask:
        ask_command(args.ask)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
