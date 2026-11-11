
import json
import statistics
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval import search, load_config, DB_DIR


# ==========================================
# CHEMINS ET PARAMÈTRES
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT / "data" / "processed" / "evaluation_dataset.jsonl"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "reports" / "evaluation_retrieval.json"
)

TOP_K = 5


# ==========================================
# CHARGEMENT DU DATASET
# ==========================================

def load_dataset():
    """Charge le jeu de questions annotées."""

    questions = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                question = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Erreur JSON à la ligne {line_number}: {error}"
                )

            questions.append(question)

    if not questions:
        raise ValueError("Le jeu de données est vide.")

    return questions


# ==========================================
# CALCUL DES MÉTRIQUES
# ==========================================

def calculate_metrics(results, expected_document_ids):
    """Calcule Recall@5, Precision@5 et MRR."""

    expected = set(expected_document_ids)

    # Documents distincts retrouvés dans le Top 5
    retrieved = []

    for chunk in results[:TOP_K]:

        document_id = chunk.get("document_id")

        if document_id and document_id not in retrieved:
            retrieved.append(document_id)

    retrieved_set = set(retrieved)

    # Recall@5
    recall = (
        len(expected & retrieved_set) / len(expected)
        if expected else 0.0
    )

    # Precision@5 au niveau des documents distincts
    precision = (
        len(expected & retrieved_set) / len(retrieved_set)
        if retrieved_set else 0.0
    )

    # MRR : rang du premier document pertinent
    reciprocal_rank = 0.0

    for rank, document_id in enumerate(retrieved, start=1):

        if document_id in expected:
            reciprocal_rank = 1 / rank
            break

    return {
        "recall_at_5": recall,
        "precision_at_5": precision,
        "mrr": reciprocal_rank
    }


# ==========================================
# ÉVALUATION D'UNE CONFIGURATION
# ==========================================

def evaluate_configuration(config_name, questions, model, client):

    print(f"\n===== CONFIGURATION {config_name} =====")

    all_metrics = []

    for question in questions:

        # Les questions sans réponse ne servent pas
        # au calcul de la pertinence documentaire.
        if not question["answer_available"]:
            continue

        results = search(
            question["question"],
            config_name,
            model,
            client,
            top_k=TOP_K
        )

        metrics = calculate_metrics(
            results,
            question["expected_document_ids"]
        )

        all_metrics.append(metrics)

        print(
            f"{question['id']} | "
            f"Recall@5 : {metrics['recall_at_5']:.2f} | "
            f"Precision@5 : {metrics['precision_at_5']:.2f} | "
            f"MRR : {metrics['mrr']:.2f}"
        )

    if not all_metrics:
        raise ValueError("Aucune question évaluable.")

    return {
        "configuration": config_name,
        "nombre_questions_evaluees": len(all_metrics),

        "recall_at_5": statistics.mean(
            metric["recall_at_5"] for metric in all_metrics
        ),

        "precision_at_5": statistics.mean(
            metric["precision_at_5"] for metric in all_metrics
        ),

        "mrr": statistics.mean(
            metric["mrr"] for metric in all_metrics
        )
    }


# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

def main():

    print("===== ÉVALUATION DU RETRIEVAL MODASTYLE =====")

    # Charger les questions
    questions = load_dataset()

    print("Nombre total de questions :", len(questions))

    evaluable_questions = [
        question for question in questions
        if question["answer_available"]
    ]

    print(
        "Questions évaluables :",
        len(evaluable_questions)
    )

    # Charger la configuration
    config = load_config()

    model_name = config["embeddings"]["model_name"]

    # Charger le modèle une seule fois
    print("\nChargement du modèle d'embeddings...")

    model = SentenceTransformer(model_name)

    # Connexion à ChromaDB
    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    results = []

    # Comparer A et B
    for config_name in ["A", "B"]:

        evaluation = evaluate_configuration(
            config_name,
            questions,
            model,
            client
        )

        results.append(evaluation)

    # Enregistrer les résultats
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:

        json.dump(
            results,
            file,
            ensure_ascii=False,
            indent=4
        )

    # Afficher les résultats finaux
    print("\n===== RÉSULTATS FINAUX =====")

    for result in results:

        print(f"\nConfiguration {result['configuration']}")

        print(
            f"Recall@5    : {result['recall_at_5']:.2%}"
        )

        print(
            f"Precision@5 : {result['precision_at_5']:.2%}"
        )

        print(
            f"MRR         : {result['mrr']:.2f}"
        )

    print("\nRésultats enregistrés dans :")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
