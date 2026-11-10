import json
import re
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "documents_extraits.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

def load_config():
    """Charge la configuration RAG."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def split_long_text(text, chunk_size, overlap):
    """Découpe un texte trop long avec chevauchement."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def split_into_chunks(content, chunk_size, overlap):
    text = re.sub(r"\n{3,}", "\n\n", content.strip())

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            min_boundary = start + int(chunk_size * 0.6)

            # Priorité aux limites des paragraphes
            boundary = text.rfind("\n\n", min_boundary, end)
            extra = 2

            # Sinon, recherche une fin de phrase
            if boundary == -1:
                boundary = text.rfind(". ", min_boundary, end)
                extra = 1

            # Sinon, recherche un espace
            if boundary == -1:
                boundary = text.rfind(" ", min_boundary, end)
                extra = 1

            if boundary != -1:
                end = boundary + extra

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        # Le prochain chunk reprend une partie du précédent
        next_start = max(start + 1, end - overlap)

        # Évite de commencer au milieu d'un mot
        space = text.find(" ", next_start, min(next_start + 40, len(text)))

        if space != -1:
            next_start = space + 1

        start = next_start

    return chunks

def load_documents():
    """Charge les documents préparés."""
    documents = []

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                documents.append(json.loads(line))

    return documents

def create_chunks(documents, config_name, settings):
    """Crée les chunks et leurs métadonnées."""
    all_chunks = []

    for document in documents:
        if document["status"] != "VALIDE_AUTOMATIQUEMENT":
            print(f"Document ignoré : {document['filename']}")
            continue

        content = document["content"]

        text_chunks = split_into_chunks(
            content,
            settings["chunk_size"],
            settings["chunk_overlap"]
        )

        for index, text in enumerate(text_chunks, start=1):
            chunk = {
                "chunk_id": (
                    f"{document['document_id']}-"
                    f"{config_name}-CHUNK-{index:03d}"
                ),
                "document_id": document["document_id"],
                "filename": document["filename"],
                "version": document["version"],
                "source": document["source"],
                "source_sha256": document["source_sha256"],
                "chunk_index": index,
                "configuration": config_name,
                "chunk_size": settings["chunk_size"],
                "chunk_overlap": settings["chunk_overlap"],
                "content": text
            }

            all_chunks.append(chunk)

    return all_chunks


def save_chunks(chunks, config_name):
    """Enregistre les chunks au format JSONL."""
    output_path = OUTPUT_DIR / f"chunks_{config_name}.jsonl"

    with open(output_path, "w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(
                json.dumps(chunk, ensure_ascii=False) + "\n"
            )

    return output_path


def main():
    config = load_config()
    documents = load_documents()

    print("===== CHUNKING MODASTYLE =====")
    print(f"Documents chargés : {len(documents)}")

    for config_name, settings in config["chunking"]["configurations"].items():
        chunks = create_chunks(documents, config_name, settings)

        output_path = save_chunks(chunks, config_name)

        print(f"\nConfiguration {config_name}")
        print(f"Taille : {settings['chunk_size']}")
        print(f"Overlap : {settings['chunk_overlap']}")
        print(f"Nombre de chunks : {len(chunks)}")
        print(f"Fichier : {output_path}")

    print("\nDécoupage terminé.")

if __name__ == "__main__":
    main()
