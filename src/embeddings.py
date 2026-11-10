
import json
from pathlib import Path

import yaml
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_chunks(config_name):
    input_path = DATA_DIR / f"chunks_{config_name}.jsonl"

    chunks = []
    with open(input_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def generate_embeddings(chunks, model, normalize):
    texts = [chunk["content"] for chunk in chunks]

    vectors = model.encode(
        texts,
        normalize_embeddings=normalize,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    results = []

    for chunk, vector in zip(chunks, vectors):
        result = chunk.copy()
        result["embedding"] = vector.tolist()
        results.append(result)

    return results


def save_embeddings(results, config_name):
    output_path = DATA_DIR / f"embeddings_{config_name}.jsonl"

    with open(output_path, "w", encoding="utf-8") as file:
        for result in results:
            file.write(json.dumps(result, ensure_ascii=False) + "\n")

    return output_path


def main():
    config = load_config()

    model_name = config["embeddings"]["model_name"]
    normalize = config["embeddings"]["normalize_embeddings"]
    expected_dimension = config["embeddings"]["dimension"]

    print("===== EMBEDDINGS MODASTYLE =====")
    print(f"Modèle : {model_name}")

    print("\nChargement du modèle...")
    model = SentenceTransformer(model_name)

    actual_dimension = model.get_sentence_embedding_dimension()

    if actual_dimension != expected_dimension:
        raise ValueError(
            f"Dimension incorrecte : {actual_dimension}, "
            f"attendu : {expected_dimension}"
        )

    print(f"Dimension des embeddings : {actual_dimension}")

    for config_name in config["chunking"]["configurations"]:
        print(f"\nConfiguration {config_name}")

        chunks = load_chunks(config_name)
        results = generate_embeddings(chunks, model, normalize)
        output_path = save_embeddings(results, config_name)

        print(f"Chunks traités : {len(results)}")
        print(f"Fichier créé : {output_path}")

    print("\nGénération des embeddings terminée.")


if __name__ == "__main__":
    main()
