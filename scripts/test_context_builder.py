
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval import load_config, search
from src.context_builder import build_context


def main():
    config = load_config()
    model_name = config["embeddings"]["model_name"]

    print("Chargement du modèle...")
    model = SentenceTransformer(model_name)

    db_dir = PROJECT_ROOT / "data" / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir))

    question = "Quel est le délai de livraison à Fès ?"

    # 1. Récupération des passages
    retrieved_chunks = search(
        question=question,
        config_name="A",
        model=model,
        client=client,
        top_k=5
    )

    # 2. Filtrage et assemblage du contexte
    result = build_context(question, retrieved_chunks)

    context = result["context"]
    references = result["references"]
    filtered_chunks = result["filtered_chunks"]

    print("\n========== BILAN ==========")
    print("Chunks récupérés :", len(retrieved_chunks))
    print("Chunks conservés :", len(filtered_chunks))
    print("Chunks écartés :", len(retrieved_chunks) - len(filtered_chunks))

    print("\n========== CONTEXTE ASSEMBLÉ ==========")
    print(context)

    print("\n========== RÉFÉRENCES DOCUMENTAIRES ==========")
    for reference in references:
        print(
            reference["document_id"],
            "|",
            reference["filename"],
            "| Version :",
            reference["version"]
        )


if __name__ == "__main__":
    main()
