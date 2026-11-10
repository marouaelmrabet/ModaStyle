
import sys
from pathlib import Path

# Ajouter la racine du projet au chemin de recherche Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generation import generate_answer, FALLBACK_MESSAGE


question = "Quel est le délai de livraison à Fès ?"

context = """
[Source : livraison.md | Document : MS-DOC-003 | Version : 1.0]

Les délais de livraison pour les principales villes,
dont Fès, sont de 2 à 3 jours ouvrables.
"""

print("========== QUESTION ==========")
print(question)

print("\n========== REPONSE GROQ ==========")

answer = generate_answer(question, context)
print(answer)

print("\n========== TEST SANS CONTEXTE ==========")

answer_without_context = generate_answer(
    "Quels sont les horaires de la boutique ?",
    ""
)

print(answer_without_context)

print(
    "\nRéponse de secours respectée :",
    answer_without_context == FALLBACK_MESSAGE
)
