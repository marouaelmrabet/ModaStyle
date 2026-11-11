
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
import yaml
from sentence_transformers import SentenceTransformer

from src.retrieval import search


QUESTIONS_PATH = (
    PROJECT_ROOT / "data" / "processed" / "experiment_questions.jsonl"
)
CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"


def load_questions():
    questions = []

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                questions.append(json.loads(line))

    return questions


def load_model():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    model_name = config["embeddings"]["model_name"]
    return SentenceTransformer(model_name)


def evaluate_configuration(config_name, questions, model, client):
    hits = 0
    total = len(questions)
    total_time = 0
    precision_scores = []
    total_unique_docs = 0

    print(f"\n========== CONFIGURATION {config_name} ==========")

    for item in questions:
        start = time.perf_counter()

        results = search(
            question=item["question"],
            config_name=config_name,
            model=model,
            client=client,
            top_k=5
        )

        elapsed = time.perf_counter() - start
        total_time += elapsed

        expected_ids = set(item["expected_document_ids"])
        retrieved_ids = {
            chunk["document_id"] for chunk in results
        }

        relevant_docs = expected_ids.intersection(retrieved_ids)
        hit = bool(relevant_docs)

        if hit:
            hits += 1

        precision = (
            len(relevant_docs) / len(retrieved_ids)
            if retrieved_ids else 0.0
        )

        precision_scores.append(precision)
        total_unique_docs += len(retrieved_ids)

        print(f"\n{item['id']} : {item['question']}")
        print("Documents attendus :", sorted(expected_ids))
        print("Documents récupérés :", sorted(retrieved_ids))
        print("Hit@5 :", hit)
        print(f"Précision documentaire : {precision * 100:.1f}%")
        print(f"Temps : {elapsed:.3f} secondes")

    hit_rate = hits / total if total else 0

    average_precision = (
        sum(precision_scores) / total
        if total else 0
    )

    average_time = total_time / total if total else 0

    average_unique_docs = (
        total_unique_docs / total
        if total else 0
    )

    return {
        "configuration": config_name,
        "hits": hits,
        "total": total,
        "hit_at_5": round(hit_rate, 4),
        "document_precision": round(average_precision, 4),
        "average_unique_documents": round(average_unique_docs, 2),
        "average_time_seconds": round(average_time, 4)
    }


def main():
    questions = load_questions()

    if not questions:
        print("ERREUR : aucune question de test trouvée.")
        return

    print("Nombre de questions :", len(questions))

    model = load_model()
    client = chromadb.PersistentClient(path=str(DB_DIR))

    results = []

    for config_name in ["A", "B"]:
        result = evaluate_configuration(
            config_name,
            questions,
            model,
            client
        )
        results.append(result)

    print("\n========== COMPARAISON FINALE ==========")

    for result in results:
        print(
            f"\nConfiguration {result['configuration']}\n"
            f"Hit@5 : {result['hits']}/{result['total']} "
            f"({result['hit_at_5'] * 100:.1f} %)\n"
            f"Précision documentaire moyenne : "
            f"{result['document_precision'] * 100:.1f} %\n"
            f"Nombre moyen de documents distincts : "
            f"{result['average_unique_documents']:.2f}\n"
            f"Temps moyen : "
            f"{result['average_time_seconds']:.3f} secondes"
        )

    output_path = PROJECT_ROOT / "reports" / "experiment_retrieval.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print("\nRésultats enregistrés dans :", output_path)


if __name__ == "__main__":
    main()
