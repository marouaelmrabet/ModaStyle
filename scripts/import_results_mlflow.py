
import json
from pathlib import Path

import mlflow
import yaml


ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
CONFIG_PATH = ROOT / "configs" / "rag_config.yaml"
MANIFEST_PATH = ROOT / "data" / "processed" / "manifest.json"

EXPERIMENT_NAME = "ModaStyle_RAG"
TRACKING_DB = ROOT / "mlflow.db"
ARTIFACT_DIR = ROOT / "mlartifacts"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def configure_mlflow():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    tracking_uri = f"sqlite:///{TRACKING_DB.as_posix()}"
    mlflow.set_tracking_uri(tracking_uri)

    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:
        mlflow.create_experiment(
            EXPERIMENT_NAME,
            artifact_location=ARTIFACT_DIR.resolve().as_uri()
        )

    mlflow.set_experiment(EXPERIMENT_NAME)


def log_common_information(config, config_name, phase):
    chunking = config["chunking"]["configurations"][config_name]

    mlflow.log_params({
        "phase": phase,
        "configuration": config_name,
        "chunk_size": chunking["chunk_size"],
        "chunk_overlap": chunking["chunk_overlap"],
        "embedding_model": config["embeddings"]["model_name"],
        "embedding_dimension": config["embeddings"]["dimension"],
        "distance_metric": config["vector_store"]["distance_metric"],
        "results_origin": "existing_evaluation_reports"
    })

    mlflow.set_tags({
        "project": "ModaStyle",
        "historical_import": "true",
        "execution_date": "not_recorded"
    })


def log_existing_artifacts(paths):
    for path in paths:
        if path.exists() and path.is_file():
            mlflow.log_artifact(str(path), artifact_path="sources")
        else:
            print(f"Fichier justificatif absent (ignore) : {path}")


def main():
    required_files = [
        CONFIG_PATH,
        REPORTS / "experiment_retrieval.json",
        REPORTS / "evaluation_retrieval.json",
        REPORTS / "evaluation_answer_metrics.json",
    ]

    missing = [path for path in required_files if not path.exists()]

    if missing:
        raise FileNotFoundError(
            "Fichiers obligatoires absents :\n"
            + "\n".join(str(path) for path in missing)
        )

    config = load_config()
    phase6 = load_json(REPORTS / "experiment_retrieval.json")
    phase7_retrieval = load_json(REPORTS / "evaluation_retrieval.json")
    phase7_answers = load_json(REPORTS / "evaluation_answer_metrics.json")

    configure_mlflow()

    common_artifacts = [
        CONFIG_PATH,
        MANIFEST_PATH,
        REPORTS / "registre_experimentations.md",
    ]

    phase6_artifacts = common_artifacts + [
        REPORTS / "experiment_retrieval.json",
        REPORTS / "rapport_experimentation_phase6.md",
    ]

    phase7_artifacts = common_artifacts + [
        REPORTS / "evaluation_retrieval.json",
        REPORTS / "evaluation_answer_metrics.json",
        REPORTS / "evaluation_answers.json",
        REPORTS / "rapport_evaluation_phase7.md",
    ]

    for result in phase6:
        name = result["configuration"]

        with mlflow.start_run(run_name=f"EXP-001_{name}"):
            log_common_information(config, name, "phase6")

            mlflow.log_params({
                "number_of_questions": result["total"]
            })

            mlflow.log_metrics({
                "hit_at_5": result["hit_at_5"],
                "document_precision": result["document_precision"],
                "average_unique_documents": result["average_unique_documents"],
                "average_time_seconds": result["average_time_seconds"],
            })

            log_existing_artifacts(phase6_artifacts)

            print(f"Importation terminee : EXP-001_{name}")

    for result in phase7_retrieval:
        name = result["configuration"]
        answers = phase7_answers[name]

        with mlflow.start_run(run_name=f"EXP-002_{name}"):
            log_common_information(config, name, "phase7")

            mlflow.log_params({
                "retrieval_questions": result["nombre_questions_evaluees"],
                "answer_questions": answers["nombre_questions"],
            })

            mlflow.log_metrics({
                "recall_at_5": result["recall_at_5"],
                "precision_at_5": result["precision_at_5"],
                "mrr": result["mrr"],
                "correctness_pct": answers["scores"]["correctness"]["pourcentage"],
                "faithfulness_pct": answers["scores"]["faithfulness"]["pourcentage"],
                "relevance_pct": answers["scores"]["relevance"]["pourcentage"],
                "global_score_pct": answers["score_global"]["pourcentage"],
            })

            log_existing_artifacts(phase7_artifacts)

            print(f"Importation terminee : EXP-002_{name}")

    print("\nImportation MLflow terminee.")
    print("Experience :", EXPERIMENT_NAME)
    print("Base de suivi :", TRACKING_DB)


if __name__ == "__main__":
    main()
