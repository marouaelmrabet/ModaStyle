
from pathlib import Path

import chromadb
import yaml
from sentence_transformers import SentenceTransformer

from src.context_builder import build_context
from src.generation import generate_answer
from src.retrieval import search


# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "configs" / "rag_config.yaml"
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"


class RAGPipeline:
    """
    Pipeline RAG complet de ModaStyle.

    Il assure :
    - la recherche documentaire ;
    - le filtrage des passages ;
    - la construction du contexte ;
    - la génération de la réponse.
    """

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

        # Vérifier que la collection existe
        collection_name = f"modastyle_{self.config_name.lower()}"

        try:
            self.client.get_collection(name=collection_name)
        except Exception as error:
            raise RuntimeError(
                f"La collection {collection_name} est introuvable. "
                "Vérifie le stockage vectoriel."
            ) from error

    def ask(self, question):
        """
        Traite une question et retourne
        une réponse avec les références documentaires.
        """

        if not question or not question.strip():
            raise ValueError(
                "La question ne peut pas être vide."
            )

        question = question.strip()

        # 1. Recherche documentaire
        retrieved_chunks = search(
            question=question,
            config_name=self.config_name,
            model=self.embedding_model,
            client=self.client,
            top_k=self.top_k
        )

        # 2. Filtrage et construction du contexte
        context_data = build_context(
            question,
            retrieved_chunks
        )

        context = context_data["context"]
        references = context_data["references"]

        # 3. Génération de la réponse
        answer = generate_answer(
            question=question,
            context=context
        )

        # 4. Retourner les résultats
        return {
            "question": question,
            "answer": answer,
            "references": references,
            "retrieved_count": len(retrieved_chunks),
            "filtered_count": len(
                context_data["filtered_chunks"]
            ),
            "configuration": self.config_name
        }


if __name__ == "__main__":

    pipeline = RAGPipeline(
        config_name="A",
        top_k=5
    )

    question = "Quel est le délai de livraison à Fès ?"

    result = pipeline.ask(question)

    print("\n========== QUESTION ==========")
    print(result["question"])

    print("\n========== REPONSE ==========")
    print(result["answer"])

    print("\n========== REFERENCES DOCUMENTAIRES ==========")

    for reference in result["references"]:
        print(
            f"- {reference['document_id']} | "
            f"{reference['filename']} | "
            f"Version {reference['version']}"
        )

    print("\n========== INFORMATIONS DU PIPELINE ==========")
    print("Configuration :", result["configuration"])
    print("Passages récupérés :", result["retrieved_count"])
    print("Passages retenus :", result["filtered_count"])
