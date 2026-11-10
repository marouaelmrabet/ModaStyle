
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval import load_config, search
from src.relevance_filter import filter_relevant_chunks


def main():

    config = load_config()
    model_name = config["embeddings"]["model_name"]

    print("Chargement du modèle...")
    model = SentenceTransformer(model_name)

    db_dir = PROJECT_ROOT / "data" / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir))

    question = "Quel est le délai de livraison à Fès ?"

    # Étape 1 : Retrieval
    chunks = search(
        question=question,
        config_name="A",
        model=model,
        client=client,
        top_k=5
    )

    # Étape 2 : Filtrage
    relevant_chunks = filter_relevant_chunks(
        question,
        chunks
    )

    # Affichage des résultats
    print("\n========== BILAN DU FILTRAGE ==========")
    print("Chunks récupérés :", len(chunks))
    print("Chunks conservés :", len(relevant_chunks))
    print("Chunks écartés :", len(chunks) - len(relevant_chunks))

    print("\n========== CHUNKS CONSERVÉS ==========")

    for chunk in relevant_chunks:
        print("\nDocument :", chunk["filename"])
        print("Chunk :", chunk["chunk_id"])
        print("Score de pertinence :", chunk["relevance_score"])
        print("Termes correspondants :", chunk["matched_terms"])


if __name__ == "__main__":
    main()
