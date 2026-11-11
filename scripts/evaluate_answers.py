
import json
from pathlib import Path

from src.rag_pipeline import RAGPipeline


# ==========================================
# 1. CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT / "data" / "processed" / "evaluation_dataset.jsonl"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "reports" / "evaluation_answers.json"
)

CONFIGURATIONS = ["A", "B"]

FALLBACK_TEXT = (
    "Je ne dispose pas de cette information dans la documentation "
    "de ModaStyle. Veuillez contacter notre service client pour "
    "obtenir davantage de précisions."
)


# ==========================================
# 2. CHARGEMENT DU DATASET
# ==========================================

def load_dataset():

    questions = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                questions.append(json.loads(line))

            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Erreur JSON ligne {line_number}: {error}"
                )

    if not questions:
        raise ValueError("Le jeu de données est vide.")

    return questions


# ==========================================
# 3. ÉVALUATION D'UNE CONFIGURATION
# ==========================================

def evaluate_configuration(config_name, questions):

    print(f"\n===== CONFIGURATION {config_name} =====")

    # Initialiser le pipeline
    pipeline = RAGPipeline(
        config_name=config_name,
        top_k=5
    )

    evaluation_results = []

    for index, question_data in enumerate(questions, start=1):

        question = question_data["question"]

        print(
            f"\nQuestion {index}/{len(questions)} : "
            f"{question_data['id']}"
        )

        try:

            # Exécuter le pipeline RAG
            result = pipeline.ask(question)

            answer = result["answer"]

            # Vérifier la présence de la réponse de repli
            fallback_observed = (
                FALLBACK_TEXT.lower() in answer.lower()
            )

            evaluation = {
                "id": question_data["id"],
                "question": question,
                "answer_available": question_data["answer_available"],
                "reference_answer": question_data["reference_answer"],
                "key_facts": question_data["key_facts"],
                "generated_answer": answer,
                "references": result["references"],
                "retrieved_count": result["retrieved_count"],
                "filtered_count": result["filtered_count"],
                "blocked": result["blocked"],
                "fallback_expected": not question_data["answer_available"],
                "fallback_observed": fallback_observed,

                # Scores à compléter après vérification humaine
                "manual_evaluation": {
                    "correctness": None,
                    "faithfulness": None,
                    "relevance": None,
                    "comment": ""
                },

                "error": None
            }

            print("Réponse générée :", answer)

            print(
                "Nombre de références :",
                len(result["references"])
            )

        except Exception as error:

            print("ERREUR :", str(error))

            evaluation = {
                "id": question_data["id"],
                "question": question,
                "answer_available": question_data["answer_available"],
                "reference_answer": question_data["reference_answer"],
                "key_facts": question_data["key_facts"],
                "generated_answer": None,
                "references": [],
                "retrieved_count": 0,
                "filtered_count": 0,
                "blocked": False,
                "fallback_expected": not question_data["answer_available"],
                "fallback_observed": False,
                "manual_evaluation": {
                    "correctness": None,
                    "faithfulness": None,
                    "relevance": None,
                    "comment": ""
                },
                "error": str(error)
            }

        evaluation_results.append(evaluation)

    return {
        "configuration": config_name,
        "nombre_questions": len(evaluation_results),
        "resultats": evaluation_results
    }


# ==========================================
# 4. PROGRAMME PRINCIPAL
# ==========================================

def main():

    print("===== ÉVALUATION DES RÉPONSES MODASTYLE =====")

    questions = load_dataset()

    print("Nombre de questions :", len(questions))

    results = []

    for config_name in CONFIGURATIONS:

        evaluation = evaluate_configuration(
            config_name,
            questions
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

    print("\n===== ÉVALUATION TERMINÉE =====")

    for result in results:

        print(
            f"Configuration {result['configuration']} : "
            f"{result['nombre_questions']} questions"
        )

    print("\nRésultats enregistrés dans :")
    print(OUTPUT_PATH)

    print(
        "\nLes scores manuels restent à compléter "
        "après vérification des réponses."
    )


if __name__ == "__main__":
    main()
