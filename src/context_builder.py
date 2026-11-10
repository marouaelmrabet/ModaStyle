
from src.relevance_filter import filter_relevant_chunks


def build_context(question, retrieved_chunks):
    # Étape 1 : conserver uniquement les passages pertinents
    relevant_chunks = filter_relevant_chunks(
        question,
        retrieved_chunks
    )

    context_parts = []
    references = []
    seen_references = set()

    # Étape 2 : assembler le contexte et les références
    for chunk in relevant_chunks:
        content = chunk.get("content", "")
        filename = chunk.get("filename", "Inconnu")
        document_id = chunk.get("document_id", "Inconnu")
        version = chunk.get("version", "Inconnue")
        chunk_id = chunk.get("chunk_id", "Inconnu")

        if not content.strip():
            continue

        context_part = (
            f"[Source : {filename} | "
            f"Document : {document_id} | "
            f"Version : {version} | "
            f"Chunk : {chunk_id}]\n"
            f"{content}"
        )

        context_parts.append(context_part)

        reference_key = (document_id, version, filename)

        if reference_key not in seen_references:
            references.append({
                "document_id": document_id,
                "filename": filename,
                "version": version,
                "source": chunk.get("source")
            })
            seen_references.add(reference_key)

    context = "\n\n---\n\n".join(context_parts)

    return {
        "context": context,
        "references": references,
        "filtered_chunks": relevant_chunks
    }
