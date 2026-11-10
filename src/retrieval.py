
from pathlib import Path

import chromadb
import yaml
from sentence_transformers import SentenceTransformer


# Chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"


def load_config():
    """Charge la configuration du projet RAG."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def search(question, config_name, model, client, top_k=5):
    """
    Recherche les chunks les plus pertinents dans ChromaDB.

    Retourne une liste de résultats structurés
    pour permettre leur utilisation par les étapes suivantes.
    """

    collection_name = f"modastyle_{config_name.lower()}"
    collection = client.get_collection(name=collection_name)

    # Transformer la question en vecteur numérique
    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # Rechercher les chunks les plus proches
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    # Structurer les résultats
    retrieved_chunks = []

    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]

        chunk = {
            "chunk_id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "document_id": metadata.get("document_id"),
            "filename": metadata.get("filename"),
            "version": metadata.get("version"),
            "source": metadata.get("source"),
            "source_sha256": metadata.get("source_sha256"),
            "chunk_index": metadata.get("chunk_index"),
            "configuration": metadata.get("configuration")
        }

        retrieved_chunks.append(chunk)

    return retrieved_chunks


def main():
    config = load_config()
    model_name = config["embeddings"]["model_name"]

    print("===== RECHERCHE SEMANTIQUE MODASTYLE =====")
    print("Chargement du modèle...")

    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=str(DB_DIR))

    question = "Quel est le délai de livraison à Fès ?"

    print("\nQuestion client :", question)

    # Comparaison des deux configurations de découpage
    for config_name in ["A", "B"]:
        retrieved_chunks = search(
            question,
            config_name,
            model,
            client,
            top_k=5
        )

        print(f"\n===== CONFIGURATION {config_name} =====")

        for i, chunk in enumerate(retrieved_chunks, start=1):
            print(f"\nRésultat {i}")
            print("Document :", chunk["filename"])
            print("ID document :", chunk["document_id"])
            print("ID du chunk :", chunk["chunk_id"])
            print("Version :", chunk["version"])
            print("Distance cosinus :", round(chunk["distance"], 4))
            print("Contenu :", chunk["content"])


if __name__ == "__main__":
    main()
