import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.context_builder import build_context
from src.generation import generate_answer


question = "Quel est le délai de livraison à Fès ?"

# Deux documents de test contenant volontairement
# des informations contradictoires.

test_chunks = [
    {
        "chunk_id": "TEST-001",
        "content": (
            "Le délai de livraison à Fès est de 2 jours ouvrables."
        ),
        "document_id": "MS-TEST-001",
        "filename": "livraison_test_1.md",
        "version": "1.0",
        "source": "test",
    },
    {
        "chunk_id": "TEST-002",
        "content": (
            "Le délai de livraison à Fès est de 5 jours ouvrables."
        ),
        "document_id": "MS-TEST-002",
        "filename": "livraison_test_2.md",
        "version": "1.0",
        "source": "test",
    },
]

context_data = build_context(question, test_chunks)

print("\n========== QUESTION ==========")
print(question)

print("\n========== PASSAGES RETENUS ==========")
for chunk in context_data["filtered_chunks"]:
    print("-", chunk["document_id"], ":", chunk["content"])

print("\n========== REPONSE DU MODELE ==========")
answer = generate_answer(
    question=question,
    context=context_data["context"]
)
print(answer)

print("\n========== REFERENCES ==========")
for reference in context_data["references"]:
    print("-", reference["document_id"], "|", reference["filename"])