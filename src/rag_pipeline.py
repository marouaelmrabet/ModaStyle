
from pathlib import Path

import chromadb
import yaml
from sentence_transformers import SentenceTransformer

from src.input_guard import is_suspicious_input
from src.context_builder import build_context
from src.generation import generate_answer
from src.retrieval import search


# ==================================================
# 1. CONFIGURATION DU PROJET
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"


# ==================================================
# 2. CLASSE PRINCIPALE DU PIPELINE RAG
# ==================================================

class RAGPipeline:

    """
    Pipeline RAG complet de ModaStyle.

    Il assure :
    - la vérification de sécurité des questions ;
    - la recherche documentaire ;
    - le filtrage des passages ;
    - la construction du contexte ;
    - la génération de la réponse avec Groq.
    """

    # ----------------------------------------------
    # Initialisation
    # ----------------------------------------------

    def __init__(self, config_name="A", top_k=5):

        self.config_name = config_name.upper()
        self.top_k = top_k

        # Vérifier la configuration
        if self.config_name not in ["A", "B"]:
            raise ValueError(
                "La configuration doit être A ou B."
            )

        # Charger la configuration YAML
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        # Charger le modèle d'embeddings
        model_name = self.config["embeddings"]["model_name"]

        self.embedding_model = SentenceTransformer(model_name)

        # Connexion à ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(DB_DIR)
        )

        # Vérifier l'existence de la collection
        collection_name = f"modastyle_{self.config_name.lower()}"

        try:
            self.client.get_collection(name=collection_name)

        except Exception as error:
            raise RuntimeError(
                f"La collection {collection_name} est introuvable. "
                "Vérifie le stockage vectoriel."
            ) from error

    # ----------------------------------------------
    # Traitement d'une question
    # ----------------------------------------------

    def ask(self, question):

        """
        Traite une question et retourne
        une réponse avec les références documentaires.
        """

        # Vérifier que la question n'est pas vide
        if not question or not question.strip():
            raise ValueError(
                "La question ne peut pas être vide."
            )

        question = question.strip()

        # ------------------------------------------
        # 1. Vérification de sécurité
        # ------------------------------------------

        if is_suspicious_input(question):

            return {
                "question": question,
                "answer": (
                    "Je ne peux pas traiter cette demande. "
                    "Je suis uniquement destiné à répondre "
                    "aux questions concernant ModaStyle."
                ),
                "references": [],
                "retrieved_count": 0,
                "filtered_count": 0,
                "configuration": self.config_name,
                "blocked": True
            }

        # ------------------------------------------
        # 2. Recherche documentaire
        # ------------------------------------------

        retrieved_chunks = search(
            question=question,
            config_name=self.config_name,
            model=self.embedding_model,
            client=self.client,
            top_k=self.top_k
        )

        # ------------------------------------------
        # 3. Construction du contexte
        # ------------------------------------------

        context_data = build_context(
            question,
            retrieved_chunks
        )

        context = context_data["context"]
        references = context_data["references"]

        # ------------------------------------------
        # 4. Génération de la réponse avec Groq
        # ------------------------------------------

        answer = generate_answer(
            question=question,
            context=context
        )

        # ------------------------------------------
        # 5. Retourner les résultats
        # ------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "references": references,
            "retrieved_count": len(retrieved_chunks),
            "filtered_count": len(
                context_data["filtered_chunks"]
            ),
            "configuration": self.config_name,
            "blocked": False
        }


# ==================================================
# 3. EXÉCUTION DIRECTE DU PIPELINE
# ==================================================

if __name__ == "__main__":

    # Initialiser le pipeline
    pipeline = RAGPipeline(
        config_name="A",
        top_k=5
    )

    # Question de test
    question = "Quel est le délai de livraison à Fès ?"

    # Exécuter le pipeline
    result = pipeline.ask(question)

    # Afficher la question
    print("\n========== QUESTION ==========")
    print(result["question"])

    # Afficher la réponse
    print("\n========== REPONSE ==========")
    print(result["answer"])

    # Afficher les références
    print("\n========== REFERENCES DOCUMENTAIRES ==========")

    if result["references"]:

        for reference in result["references"]:

            print(
                f"- {reference['document_id']} | "
                f"{reference['filename']} | "
                f"Version {reference['version']}"
            )

    else:
        print("Aucune référence documentaire.")

    # Afficher les informations techniques
    print("\n========== INFORMATIONS DU PIPELINE ==========")

    print("Configuration :", result["configuration"])
    print("Passages récupérés :", result["retrieved_count"])
    print("Passages retenus :", result["filtered_count"])
    print("Question bloquée :", result["blocked"])
