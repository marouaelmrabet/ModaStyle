
import json
from pathlib import Path

import chromadb
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_embeddings(config_name):
    input_path = DATA_DIR / f"embeddings_{config_name}.jsonl"

    records = []
    with open(input_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def create_collection(client, config_name, distance_metric):
    collection_name = f"modastyle_{config_name.lower()}"

    # Supprimer l'ancienne collection pour reconstruire un index propre
    existing_names = [
        collection.name for collection in client.list_collections()
    ]

    if collection_name in existing_names:
        client.delete_collection(collection_name)

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": distance_metric}
    )

    return collection


def store_embeddings(collection, records):
    ids = [record["chunk_id"] for record in records]
    documents = [record["content"] for record in records]
    embeddings = [record["embedding"] for record in records]

    metadatas = []

    for record in records:
        metadatas.append({
            "document_id": record["document_id"],
            "filename": record["filename"],
            "version": record["version"],
            "source_sha256": record["source_sha256"],
            "chunk_index": record["chunk_index"],
            "configuration": record["configuration"],
            "chunk_size": record["chunk_size"],
            "chunk_overlap": record["chunk_overlap"]
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def main():
    config = load_config()

    distance_metric = config["vector_store"]["distance_metric"]

    print("===== CHROMADB MODASTYLE =====")

    DB_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(DB_DIR))

    for config_name in config["chunking"]["configurations"]:
        print(f"\nConfiguration {config_name}")

        records = load_embeddings(config_name)

        collection = create_collection(
            client,
            config_name,
            distance_metric
        )

        store_embeddings(collection, records)

        print("Collection :", collection.name)
        print("Chunks stockés :", collection.count())
        print("Distance :", distance_metric)

    print("\nStockage vectoriel terminé.")
    print("Emplacement :", DB_DIR)


if __name__ == "__main__":
    main()
