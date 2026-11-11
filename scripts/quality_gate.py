
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

MANIFEST_PATH = ROOT / "data" / "processed" / "manifest.json"
CONFIG_PATH = ROOT / "configs" / "rag_config.yaml"
RETRIEVAL_PATH = REPORTS / "evaluation_retrieval.json"
ANSWERS_PATH = REPORTS / "evaluation_answer_metrics.json"

THRESHOLDS = {
    "recall_at_5": 0.95,
    "correctness": 75.0,
    "faithfulness": 90.0,
    "relevance": 80.0,
    "global_score": 80.0,
}


results = []


def add_result(name, passed, details):
    results.append({
        "controle": name,
        "statut": "PASS" if passed else "FAIL",
        "details": details,
    })

    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} : {details}")


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_tests():
    print("\n--- 1. Tests automatises ---")

    process = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    output = process.stdout + process.stderr
    passed = process.returncode == 0

    add_result(
        "Tests automatises",
        passed,
        "Tous les tests sont reussis"
        if passed else "Au moins un test a echoue",
    )

    if not passed:
        print(output)


def check_corpus():
    print("\n--- 2. Integrite du corpus ---")

    try:
        manifest = load_json(MANIFEST_PATH)
        documents = manifest["documents"]

        count_ok = (
            manifest["document_count"] == len(documents)
            and len(documents) == 7
        )

        add_result(
            "Nombre de documents",
            count_ok,
            f"{len(documents)} documents declares",
        )

        all_valid = True
        errors = []

        for document in documents:
            source_path = ROOT / document["source"]

            if not source_path.is_file():
                all_valid = False
                errors.append(
                    f"Fichier absent : {document['source']}"
                )
                continue

            content_hash = hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest()

            if content_hash != document["source_sha256"]:
                all_valid = False
                errors.append(
                    f"Hash incorrect : {document['filename']}"
                )

            if document["status"] != "VALIDE_AUTOMATIQUEMENT":
                all_valid = False
                errors.append(
                    f"Document non valide : {document['filename']}"
                )

        add_result(
            "Integrite SHA-256 du corpus",
            all_valid,
            "Toutes les sources correspondent au manifeste"
            if all_valid else "; ".join(errors),
        )

    except Exception as error:
        add_result(
            "Integrite du corpus",
            False,
            str(error),
        )


def check_config():
    print("\n--- 3. Configuration RAG ---")

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        configurations = config["chunking"]["configurations"]

        valid = (
            config["project"]["name"] == "ModaStyle"
            and "A" in configurations
            and "B" in configurations
            and config["embeddings"]["dimension"] == 384
            and config["vector_store"]["distance_metric"] == "cosine"
        )

        add_result(
            "Configuration RAG",
            valid,
            "Configuration A/B et parametres essentiels valides"
            if valid else "Configuration invalide ou incomplete",
        )

    except Exception as error:
        add_result(
            "Configuration RAG",
            False,
            str(error),
        )


def check_retrieval():
    print("\n--- 4. Qualite du retrieval ---")

    try:
        evaluations = load_json(RETRIEVAL_PATH)

        for evaluation in evaluations:
            name = evaluation["configuration"]
            recall = evaluation["recall_at_5"]

            valid = (
                evaluation["nombre_questions_evaluees"] > 0
                and recall >= THRESHOLDS["recall_at_5"]
            )

            add_result(
                f"Recall@5 configuration {name}",
                valid,
                f"{recall * 100:.2f}% "
                f"(seuil : {THRESHOLDS['recall_at_5'] * 100:.0f}%)",
            )

    except Exception as error:
        add_result(
            "Evaluation retrieval",
            False,
            str(error),
        )


def check_generation():
    print("\n--- 5. Qualite de generation ---")

    try:
        evaluations = load_json(ANSWERS_PATH)

        for name, evaluation in evaluations.items():
            scores = evaluation["scores"]
            global_score = evaluation["score_global"]["pourcentage"]

            checks = {
                "Correctness": (
                    scores["correctness"]["pourcentage"],
                    THRESHOLDS["correctness"],
                ),
                "Faithfulness": (
                    scores["faithfulness"]["pourcentage"],
                    THRESHOLDS["faithfulness"],
                ),
                "Relevance": (
                    scores["relevance"]["pourcentage"],
                    THRESHOLDS["relevance"],
                ),
                "Score global": (
                    global_score,
                    THRESHOLDS["global_score"],
                ),
            }

            for metric, (value, threshold) in checks.items():
                valid = (
                    evaluation["nombre_questions"] > 0
                    and value >= threshold
                )

                add_result(
                    f"{metric} configuration {name}",
                    valid,
                    f"{value:.2f}% (seuil : {threshold:.0f}%)",
                )

    except Exception as error:
        add_result(
            "Evaluation generation",
            False,
            str(error),
        )


def save_report():
    REPORTS.mkdir(parents=True, exist_ok=True)

    failed = sum(
        1 for result in results
        if result["statut"] == "FAIL"
    )

    report = {
        "project": "ModaStyle",
        "date": datetime.now(timezone.utc).isoformat(),
        "decision": "ACCEPTE" if failed == 0 else "REJETE",
        "total_controls": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "thresholds": THRESHOLDS,
        "results": results,
    }

    output_path = REPORTS / "quality_gate_report.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\n--- Decision finale ---")
    print(f"Controles reussis : {report['passed']}")
    print(f"Controles echoues : {report['failed']}")
    print(f"Decision : {report['decision']}")
    print(f"Rapport : {output_path}")


def main():
    print("====================================")
    print(" QUALITY GATES - MODASTYLE")
    print("====================================")

    check_tests()
    check_corpus()
    check_config()
    check_retrieval()
    check_generation()
    save_report()

    if any(result["statut"] == "FAIL" for result in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
