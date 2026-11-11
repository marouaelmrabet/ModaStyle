
from src.context_builder import build_context


def make_test_chunk():
    return {
        "chunk_id": "TEST-001",
        "content": "La livraison à Fès prend 2 à 3 jours ouvrables.",
        "document_id": "MS-DOC-003",
        "filename": "livraison.md",
        "version": "1.0",
        "source": "test",
    }


def test_build_context_returns_expected_structure():
    question = "Quel est le délai de livraison à Fès ?"
    result = build_context(question, [make_test_chunk()])

    assert isinstance(result, dict)
    assert "context" in result
    assert "references" in result
    assert "filtered_chunks" in result


def test_build_context_contains_source_information():
    question = "Quel est le délai de livraison à Fès ?"
    result = build_context(question, [make_test_chunk()])

    assert "MS-DOC-003" in result["context"]
    assert "livraison.md" in result["context"]
    assert "2 à 3 jours ouvrables" in result["context"]


def test_build_context_deduplicates_references():
    question = "Quel est le délai de livraison à Fès ?"
    chunk1 = make_test_chunk()
    chunk2 = make_test_chunk()
    chunk2["chunk_id"] = "TEST-002"

    result = build_context(question, [chunk1, chunk2])

    assert len(result["references"]) == 1
    assert len(result["filtered_chunks"]) == 2


def test_build_context_with_empty_chunks():
    result = build_context("Quel est le délai de livraison ?", [])

    assert result["context"] == ""
    assert result["references"] == []
    assert result["filtered_chunks"] == []
