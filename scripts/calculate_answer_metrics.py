
import json
from pathlib import Path

INPUT_FILE = Path("reports/evaluation_answers.json")
OUTPUT_JSON = Path("reports/evaluation_answer_metrics.json")
OUTPUT_MD = Path("reports/rapport_evaluation_phase7.md")

CRITERIA = {
    "correctness": "Exactitude",
    "faithfulness": "Fidélité aux sources",
    "relevance": "Pertinence",
}


def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    results = {}

    for block in data:
        config = block["configuration"]
        questions = block["resultats"]

        if not questions:
            raise ValueError(f"Aucune question pour la configuration {config}")

        results[config] = {
            "nombre_questions": len(questions),
            "scores": {}
        }

        for criterion in CRITERIA:
            values = [
                item["manual_evaluation"][criterion]
                for item in questions
            ]

            if any(value is None for value in values):
                raise ValueError(
                    f"Notes manquantes : {criterion}, configuration {config}"
                )

            results[config]["scores"][criterion] = {
                "total": sum(values),
                "moyenne": round(sum(values) / len(values), 2),
                "pourcentage": round(
                    sum(values) / (2 * len(values)) * 100, 2
                )
            }

        all_scores = [
            item["manual_evaluation"][criterion]
            for item in questions
            for criterion in CRITERIA
        ]

        results[config]["score_global"] = {
            "moyenne_sur_2": round(
                sum(all_scores) / len(all_scores), 2
            ),
            "pourcentage": round(
                sum(all_scores) / (2 * len(all_scores)) * 100, 2
            )
        }

    OUTPUT_JSON.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    lines = [
        "# Rapport d'évaluation des réponses — Phase 7",
        "",
        "## Méthode",
        "",
        "Les réponses des configurations A et B ont été évaluées sur trois "
        "critères : exactitude, fidélité aux sources et pertinence.",
        "Chaque critère reçoit une note de 0 à 2.",
        "Les moyennes sont calculées sur les 15 questions de chaque configuration.",
        "",
        "## Résultats",
        "",
        "| Critère | Configuration A | Configuration B |",
        "|---|---:|---:|",
    ]

    for criterion, label in CRITERIA.items():
        a = results["A"]["scores"][criterion]["moyenne"]
        b = results["B"]["scores"][criterion]["moyenne"]
        lines.append(f"| {label} | {a}/2 | {b}/2 |")

    a_global = results["A"]["score_global"]
    b_global = results["B"]["score_global"]

    lines.extend([
        "",
        "## Score global",
        "",
        f"- Configuration A : {a_global['moyenne_sur_2']}/2 "
        f"({a_global['pourcentage']} %).",
        f"- Configuration B : {b_global['moyenne_sur_2']}/2 "
        f"({b_global['pourcentage']} %).",
        "",
        "## Interprétation",
        "",
        "Les résultats obtenus avec cette grille donnent un avantage "
        "à la configuration B sur le score global.",
        "La configuration A présente toutefois des erreurs notables, "
        "notamment une contradiction de prix pour la question Q09 "
        "et des refus injustifiés pour Q05 et Q11.",
        "La configuration B répond correctement à davantage de questions, "
        "mais certaines formulations contiennent des éléments "
        "qui ne sont pas explicitement documentés.",
        "",
        "## Limites",
        "",
        "- Le jeu d'évaluation contient seulement 15 questions.",
        "- Les notes sont des propositions à vérifier humainement.",
        "- Les critères comportent une part de jugement subjectif.",
        "- Les résultats ne garantissent pas les performances sur "
        "toutes les questions possibles.",
        "",
        "Les scores doivent être considérés comme préliminaires "
        "tant que les annotations n'ont pas été validées.",
    ])

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("===== RÉSULTATS DE L'ÉVALUATION =====")

    for config in ("A", "B"):
        print(f"\nConfiguration {config}")
        for criterion, label in CRITERIA.items():
            score = results[config]["scores"][criterion]
            print(
                f"{label} : {score['moyenne']}/2 "
                f"({score['pourcentage']} %)"
            )

        global_score = results[config]["score_global"]
        print(
            f"Score global : {global_score['moyenne_sur_2']}/2 "
            f"({global_score['pourcentage']} %)"
        )

    print("\nFichiers créés :")
    print(OUTPUT_JSON)
    print(OUTPUT_MD)


if __name__ == "__main__":
    main()
