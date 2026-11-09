
from pathlib import Path
import re
import json
import hashlib
from datetime import datetime, timezone


# --------------------------------------------------
# 1. Configuration des chemins
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Documents attendus
# --------------------------------------------------

EXPECTED_DOCUMENTS = {
    "presentation_boutique.md": "MS-DOC-001",
    "catalogue_produits.md": "MS-DOC-002",
    "livraison.md": "MS-DOC-003",
    "retours_remboursements.md": "MS-DOC-004",
    "paiements.md": "MS-DOC-005",
    "guide_tailles.md": "MS-DOC-006",
    "entretien_produits.md": "MS-DOC-007",
}


# --------------------------------------------------
# 3. Fonctions de préparation
# --------------------------------------------------

def calculate_sha256(content):
    """Calcule l'empreinte SHA-256 d'un contenu."""
    return hashlib.sha256(content).hexdigest()


def clean_content(text):
    """Nettoie le texte sans supprimer les informations utiles."""

    # Supprimer le caractère BOM éventuel
    text = text.replace("\ufeff", "")

    # Uniformiser les retours à la ligne
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Supprimer les espaces inutiles en fin de ligne
    text = "\n".join(line.rstrip() for line in text.splitlines())

    # Réduire les lignes vides excessives
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def extract_metadata(content):
    """Extrait l'identifiant et la version du document."""

    id_match = re.search(
        r"\*{0,2}\s*Identifiant du document\s*:\s*\*{0,2}\s*(MS-DOC-\d+)",
        content,
        re.IGNORECASE
    )

    version_match = re.search(
        r"\*{0,2}\s*Version(?: de l'inventaire)?\s*:\s*\*{0,2}\s*([\d.]+)",
        content,
        re.IGNORECASE
    )

    document_id = id_match.group(1) if id_match else None
    version = version_match.group(1) if version_match else None

    return document_id, version


# --------------------------------------------------
# 4. Lecture et contrôle du corpus
# --------------------------------------------------

def main():

    print("\n===== PREPARATION DU CORPUS MODASTYLE =====\n")

    results = []
    errors = []
    seen_ids = {}
    seen_hashes = {}

    timestamp = datetime.now(timezone.utc).isoformat()

    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"Le dossier du corpus est introuvable : {RAW_DIR}"
        )

    for filename, expected_id in EXPECTED_DOCUMENTS.items():

        file_path = RAW_DIR / filename

        print(f"Analyse : {filename}")

        if not file_path.exists():
            errors.append(f"Fichier manquant : {filename}")
            continue

        # Lecture du fichier original
        raw_bytes = file_path.read_bytes()
        original_content = raw_bytes.decode("utf-8-sig")

        if not original_content.strip():
            errors.append(f"Fichier vide : {filename}")
            continue

        # Empreinte du fichier original
        source_hash = calculate_sha256(raw_bytes)

        # Extraction des métadonnées
        document_id, version = extract_metadata(original_content)

        document_errors = []

        if not document_id:
            document_errors.append("Identifiant absent")
        elif document_id != expected_id:
            document_errors.append(
                f"Identifiant incorrect : {document_id}, "
                f"attendu : {expected_id}"
            )

        if not version:
            document_errors.append("Version absente")
        elif version != "1.0":
            document_errors.append(
                f"Version inattendue : {version}"
            )

        # Vérification des identifiants dupliqués
        if document_id:
            if document_id in seen_ids:
                document_errors.append(
                    f"Identifiant dupliqué : {document_id}"
                )
            else:
                seen_ids[document_id] = filename

        # Vérification des contenus identiques
        if source_hash in seen_hashes:
            document_errors.append(
                f"Contenu identique à : {seen_hashes[source_hash]}"
            )
        else:
            seen_hashes[source_hash] = filename

        # Nettoyage du texte
        cleaned_content = clean_content(original_content)

        # Empreinte du contenu nettoyé
        processed_hash = calculate_sha256(
            cleaned_content.encode("utf-8")
        )

        # Statut du document
        status = (
            "A_VERIFIER"
            if document_errors
            else "VALIDE_AUTOMATIQUEMENT"
        )

        for error in document_errors:
            errors.append(f"{filename} : {error}")

        results.append({
            "document_id": document_id,
            "filename": filename,
            "version": version,
            "source": f"data/raw/{filename}",
            "source_sha256": source_hash,
            "processed_sha256": processed_hash,
            "content": cleaned_content,
            "status": status,
            "validation_errors": document_errors
        })

    # Vérification des documents supplémentaires
    for file_path in RAW_DIR.glob("*.md"):
        if file_path.name not in EXPECTED_DOCUMENTS:
            errors.append(
                f"Document non répertorié : {file_path.name}"
            )

    # --------------------------------------------------
    # 5. Export du texte nettoyé au format JSONL
    # --------------------------------------------------

    output_file = PROCESSED_DIR / "documents_extraits.jsonl"

    with output_file.open("w", encoding="utf-8") as f:
        for document in results:
            f.write(
                json.dumps(document, ensure_ascii=False) + "\n"
            )

    # --------------------------------------------------
    # 6. Création du manifeste de provenance
    # --------------------------------------------------

    manifest = {
        "project": "ModaStyle",
        "created_at": timestamp,
        "pipeline_version": "1.0",
        "document_count": len(results),
        "documents": [
            {
                "document_id": document["document_id"],
                "filename": document["filename"],
                "version": document["version"],
                "source": document["source"],
                "source_sha256": document["source_sha256"],
                "processed_sha256": document["processed_sha256"],
                "status": document["status"]
            }
            for document in results
        ]
    }

    manifest_file = PROCESSED_DIR / "manifest.json"

    manifest_file.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    # --------------------------------------------------
    # 7. Rapport de contrôle qualité
    # --------------------------------------------------

    report = [
        "# Rapport de contrôle du corpus ModaStyle",
        "",
        f"Date du contrôle : {timestamp}",
        "",
        f"Nombre de documents analysés : {len(results)}",
        "",
        f"Nombre d'anomalies détectées : {len(errors)}",
        "",
        "## Anomalies",
        ""
    ]

    if errors:
        report.extend([f"- {error}" for error in errors])
    else:
        report.append(
            "Aucune anomalie détectée par les contrôles automatisés."
        )

    report.extend([
        "",
        "## Documents analysés",
        ""
    ])

    for document in results:
        report.append(
            f"- {document['filename']} : "
            f"{document['document_id']} — "
            f"version {document['version']} — "
            f"statut : {document['status']}"
        )

    report.extend([
        "",
        "## Traçabilité",
        "",
        "Les empreintes SHA-256 des fichiers sources et des contenus "
        "nettoyés sont conservées dans le manifeste.",
        "",
        "Les fichiers originaux de data/raw/ ne sont pas modifiés.",
        "",
        "Le contrôle automatisé ne remplace pas une validation "
        "manuelle de la cohérence métier des documents."
    ])

    report_file = REPORTS_DIR / "controle_qualite_corpus.md"

    report_file.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    # --------------------------------------------------
    # 8. Résultat final
    # --------------------------------------------------

    print("\n===== RESULTAT =====")
    print(f"Documents analysés : {len(results)}")
    print(f"Anomalies : {len(errors)}")
    print(f"Texte nettoyé : {output_file}")
    print(f"Manifeste : {manifest_file}")
    print(f"Rapport : {report_file}")

    if errors:
        print("\nAttention : des anomalies ont été détectées.")
    else:
        print("\nPréparation documentaire terminée.")


if __name__ == "__main__":
    main()
