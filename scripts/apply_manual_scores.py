
import json
from pathlib import Path

INPUT_FILE = Path("reports/evaluation_answers.json")

scores = {
    "A": {
        "Q01": (2, 2, 2), "Q02": (2, 2, 2),
        "Q03": (2, 2, 2), "Q04": (2, 2, 2),
        "Q05": (0, 2, 0), "Q06": (1, 2, 1),
        "Q07": (2, 2, 2), "Q08": (2, 2, 2),
        "Q09": (0, 0, 1), "Q10": (2, 2, 2),
        "Q11": (0, 2, 0), "Q12": (2, 2, 2),
        "Q13": (2, 2, 2), "Q14": (2, 2, 2),
        "Q15": (2, 2, 2),
    },
    "B": {
        "Q01": (2, 2, 2), "Q02": (2, 2, 2),
        "Q03": (2, 2, 2), "Q04": (2, 2, 2),
        "Q05": (2, 1, 2), "Q06": (2, 1, 2),
        "Q07": (2, 2, 2), "Q08": (2, 2, 2),
        "Q09": (2, 2, 2), "Q10": (2, 2, 2),
        "Q11": (0, 2, 0), "Q12": (2, 2, 2),
        "Q13": (2, 2, 2), "Q14": (2, 2, 2),
        "Q15": (2, 2, 2),
    }
}

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    backup = INPUT_FILE.with_name("evaluation_answers_backup.json")

    # Créer une sauvegarde avant toute modification
    if not backup.exists():
        backup.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    total = 0

    for block in data:
        config = block.get("configuration")

        if config not in scores:
            raise ValueError(f"Configuration inconnue : {config}")

        for item in block.get("resultats", []):
            question_id = item.get("id")

            if question_id not in scores[config]:
                raise ValueError(
                    f"Question inconnue : {question_id}, configuration {config}"
                )

            correctness, faithfulness, relevance = scores[config][question_id]

            item["manual_evaluation"] = {
                "correctness": correctness,
                "faithfulness": faithfulness,
                "relevance": relevance,
                "comment": "Note proposée, à vérifier."
            }

            total += 1

    INPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Notes ajoutées : {total}")
    print(f"Sauvegarde : {backup}")
    print("Évaluation manuelle enregistrée.")

if __name__ == "__main__":
    main()
