
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval import load_config, search
from src.context_builder import build_context
from src.generation import build_prompt


def main():
    # Charger la configuration
    config = load_config()
    model_name = config["embeddings"]["model_name"]

    # Charger le modèle d'embeddings
    print("Chargement du modèle...")
    model = SentenceTransformer(model_name)

    # Connexion à ChromaDB
    db_dir = PROJECT_ROOT / "data" / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir))

    # Question du client
    question = "Quel est le délai de livraison à Fès ?"

    print("\nQuestion :", question)

    # Étape 1 : Retrieval
    chunks = search(
        question=question,
        config_name="A",
        model=model,
        client=client,
        top_k=5
    )

    # Étape 2 : Assemblage du contexte
    context_result = build_context(chunks)

    context = context_result["context"]
    references = context_result["references"]

    # Étape 3 : Construction du prompt
    prompt = build_prompt(question, context)

    # Afficher le prompt
    print("\n========== PROMPT CONSTRUIT ==========")
    print(prompt)

    # Afficher les références disponibles
    print("\n========== RÉFÉRENCES DOCUMENTAIRES ==========")

    for reference in references:
        print(
            f"- {reference['document_id']} | "
            f"{reference['filename']} | "
            f"Version {reference['version']}"
        )


if __name__ == "__main__":
    main()
