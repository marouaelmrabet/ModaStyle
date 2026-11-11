
from src.relevance_filter import (
    normalize_text,
    tokenize,
    calculate_relevance_score,
    filter_relevant_chunks,
)


def test_normalize_text_removes_accents():
    assert normalize_text("Livraison à Fès") == "livraison a fes"


def test_tokenize_removes_stopwords():
    terms = tokenize("Quel est le délai de livraison à Fès ?")

    assert "quel" not in terms
    assert "est" not in terms
    assert "livraison" in terms
    assert "delai" in terms
    assert "fes" in terms


def test_calculate_relevance_score():
    question_terms = {"livraison", "fes", "delai"}
    content = "La livraison à Fès prend 2 à 3 jours."

    score, matched_terms = calculate_relevance_score(
        question_terms,
        content
    )

    assert matched_terms == {"livraison", "fes"}
    assert score > 0


def test_filter_relevant_chunks_excludes_irrelevant_chunks():
    question = "Quel est le délai de livraison à Fès ?"

    chunks = [
        {
            "chunk_id": "TEST-001",
            "content": "La livraison à Fès prend 2 à 3 jours.",
        },
        {
            "chunk_id": "TEST-002",
            "content": "Les moyens de paiement sont la carte bancaire et le virement.",
        },
    ]

    result = filter_relevant_chunks(question, chunks)

    assert len(result) == 1
    assert result[0]["chunk_id"] == "TEST-001"


def test_filter_relevant_chunks_sorts_by_score():
    question = "Quel est le délai de livraison à Fès ?"

    chunks = [
        {
            "chunk_id": "TEST-001",
            "content": "La livraison à Fès prend 2 à 3 jours.",
        },
        {
            "chunk_id": "TEST-002",
            "content": "Le délai de livraison à Fès est de 2 à 3 jours ouvrables.",
        },
    ]

    result = filter_relevant_chunks(question, chunks)

    assert len(result) == 2
    assert (
        result[0]["relevance_score"]
        >= result[1]["relevance_score"]
    )


def test_filter_relevant_chunks_with_empty_question():
    chunks = [
        {"chunk_id": "TEST-001", "content": "Livraison à Fès."}
    ]

    result = filter_relevant_chunks("?", chunks)

    assert result == chunks
