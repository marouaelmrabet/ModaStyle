\# ModaStyle — Assistant intelligent RAG



\## 1. Présentation du projet



ModaStyle est une boutique fictive spécialisée dans la mode au Maroc.



Ce projet consiste à développer et industrialiser un assistant conversationnel intelligent basé sur la technologie RAG (\*Retrieval-Augmented Generation\*).



L'assistant répond aux questions des clients en s'appuyant sur les documents de référence de la boutique afin de fournir des réponses pertinentes, fiables et accompagnées de sources.



L'objectif est de limiter les réponses inventées et de garantir que les informations fournies proviennent du corpus documentaire.



\## 2. Objectifs



\- Développer un assistant conversationnel destiné aux clients de ModaStyle.

\- Constituer et organiser un corpus documentaire.

\- Transformer les documents en vecteurs et les stocker dans une base vectorielle.

\- Retrouver les passages pertinents pour répondre aux questions.

\- Générer des réponses à partir du contexte documentaire.

\- Refuser de répondre lorsque les informations nécessaires sont absentes.

\- Évaluer les performances du système RAG.

\- Mettre en place des tests, un suivi des expériences et des contrôles qualité.



\## 3. Architecture technique



Le projet repose sur les composants suivants :



\- \*\*Python 3.12\*\* : langage de développement.

\- \*\*ChromaDB\*\* : stockage et recherche vectorielle.

\- \*\*Sentence Transformers\*\* : génération des embeddings avec `paraphrase-multilingual-MiniLM-L12-v2`.

\- \*\*Groq API\*\* : génération des réponses avec le modèle `openai/gpt-oss-20b`.

\- \*\*MLflow\*\* : suivi des expériences et des résultats.

\- \*\*FastAPI\*\* : mise à disposition de l'application.

\- \*\*Uvicorn\*\* : serveur d'exécution.

\- \*\*Pytest\*\* : tests automatisés.

\- \*\*Git et GitHub\*\* : gestion du code source et versionnement.

\- \*\*GitHub Actions\*\* : intégration continue.



\## 4. Organisation du projet



```text

ModaStyle/

│

├── .github/              # Configuration de l'intégration continue

├── configs/              # Configurations du pipeline RAG

├── data/

│   ├── raw/              # Documents sources

│   ├── processed/        # Manifest et données préparées

│   └── chroma\_db/        # Base vectorielle locale

├── docs/                 # Documentation du projet

├── interface/            # Interface utilisateur FastAPI

├── reports/              # Rapports et résultats d'évaluation

├── scripts/              # Scripts d'exécution et de vérification

├── src/                  # Code source du système RAG

├── tests/                # Tests automatisés

├── .env.example          # Exemple de configuration des variables

├── .gitignore            # Fichiers exclus du versionnement

├── requirements.txt      # Dépendances du projet

└── README.md             # Documentation principale

```



\## 5. Installation et configuration



\### Prérequis



\- Python 3.12

\- Git

\- Une clé API Groq valide



\### Installation



Cloner le dépôt :



```bash

git clone https://github.com/marouaelmrabet/ModaStyle.git

cd ModaStyle

```



Créer et activer un environnement virtuel :



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



Installer les dépendances :



```bash

pip install -r requirements.txt

```



\### Configuration de la clé API



Créer un fichier `.env` à la racine du projet à partir de `.env.example`, puis renseigner :



```text

GROQ\_API\_KEY=votre\_cle\_api

```



\## 6. Corpus documentaire et indexation



Le corpus documentaire contient les documents de référence de ModaStyle.



Les documents sont organisés dans `data/raw/`. Le fichier `data/processed/manifest.json` permet de conserver les informations d'inventaire et les empreintes SHA256 des documents.



Le projet compare deux configurations de découpage documentaire :



\- Configuration A : chunks de 500 caractères avec chevauchement de 100.

\- Configuration B : chunks de 800 caractères avec chevauchement de 120.



Les embeddings sont générés avec Sentence Transformers et stockés dans ChromaDB.



Les collections utilisées sont :



\- `modastyle\_a`

\- `modastyle\_b`



La base vectorielle peut être reconstruite à partir des documents sources et des scripts d'indexation du projet.



\## 7. Exécution de l'assistant



L'interface web est lancée avec :



```bash

python -m uvicorn interface.app:app --reload

```



Ouvrir ensuite l'adresse suivante dans un navigateur :



\[http://127.0.0.1:8000](http://127.0.0.1:8000)



Le client peut poser ses questions à l'assistant et recevoir des réponses fondées sur les documents disponibles.



Un endpoint de santé est également disponible :



```text

http://127.0.0.1:8000/health

```



\## 8. Évaluation du système RAG



Le projet comprend un jeu de questions permettant d'évaluer la recherche documentaire et la qualité des réponses générées.



Les deux configurations A et B ont été comparées à l'aide de métriques telles que :



\- Recall\\@5

\- Precision\\@5

\- MRR

\- Pertinence des réponses

\- Exactitude des réponses

\- Fidélité au contexte documentaire



Les résultats des expériences sont conservés dans les dossiers de rapports et de suivi du projet.



La configuration B a été retenue comme configuration par défaut à la suite de l'évaluation réalisée.



\## 9. Suivi des expériences avec MLflow



MLflow est utilisé pour suivre les expériences d'évaluation du système RAG.



Il permet de conserver les paramètres, les métriques et les résultats associés aux différentes configurations testées.



\## 10. Tests et contrôles qualité



Le projet intègre des tests automatisés avec Pytest.



Les contrôles qualité portent notamment sur :



\- Le fonctionnement du code.

\- La validité des configurations.

\- La cohérence du corpus documentaire.

\- Le stockage des documents dans ChromaDB.

\- La qualité des résultats de recherche.

\- La sécurité et le comportement de l'assistant.

\- Le bon démarrage de l'application.



Un script de contrôle qualité est disponible dans `scripts/quality\_gate.py`.



Pour lancer les tests :



```bash

python -m pytest -v

```



\## 11. Reproductibilité



Pour reproduire le projet :



1\. Récupérer le dépôt Git.

2\. Installer Python 3.12.

3\. Créer un environnement virtuel.

4\. Installer les dépendances depuis `requirements.txt`.

5\. Configurer la variable `GROQ\_API\_KEY`.

6\. Reconstruire la base vectorielle à partir du corpus source à l'aide des scripts d'indexation.

7\. Lancer les tests.

8\. Démarrer l'application FastAPI.



Les environnements virtuels, les secrets et les bases de données locales ne sont pas versionnés dans Git.



\## 12. Limites et perspectives



Le système dépend de la qualité et de la couverture du corpus documentaire.



Une information absente des documents ne peut pas être garantie par l'assistant. La qualité des réponses doit donc être contrôlée régulièrement.



Les améliorations possibles comprennent :



\- L'enrichissement du corpus documentaire.

\- L'amélioration des stratégies de recherche.

\- L'élargissement du jeu d'évaluation.

\- Le renforcement du monitoring de la latence, des erreurs et des coûts.

\- L'amélioration des contrôles de sécurité.



\## 13. Auteur et dépôt



Projet académique : industrialisation d'un assistant RAG.



Dépôt GitHub : \[https://github.com/marouaelmrabet/ModaStyle](https://github.com/marouaelmrabet/ModaStyle)



