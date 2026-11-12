# ModaStyle — Assistant intelligent basé sur RAG

## 1. Présentation du projet

ModaStyle est une boutique fictive spécialisée dans la mode au Maroc.

Ce projet consiste à développer et industrialiser un assistant conversationnel intelligent basé sur la technologie RAG (Retrieval-Augmented Generation).

L'assistant permet aux clients de poser des questions concernant les produits, les services et les conditions commerciales de ModaStyle. Il recherche les informations pertinentes dans un corpus documentaire, puis génère des réponses à partir des passages retrouvés.

L'objectif principal est de fournir des réponses pertinentes, fiables et accompagnées de références documentaires, tout en limitant les informations inventées.

## 2. Objectifs

- Développer un assistant conversationnel destiné aux clients de ModaStyle.
- Constituer et exploiter un corpus documentaire.
- Mettre en place une chaîne de recherche et de génération RAG.
- Comparer différentes configurations de découpage documentaire.
- Évaluer la qualité et la fiabilité des réponses.
- Industrialiser le projet avec des tests, des contrôles qualité et un suivi des expériences.

## 3. Technologies utilisées

| Technologie           | Utilisation                 |
| --------------------- | --------------------------- |
| Python 3.12           | Développement               |
| ChromaDB              | Base de données vectorielle |
| Sentence Transformers | Génération des embeddings   |
| MiniLM multilingue    | Modèle d'embedding          |
| Groq API              | Génération des réponses     |
| `openai/gpt-oss-20b`  | Modèle de langage           |
| FastAPI               | Interface web               |
| MLflow                | Suivi des expériences       |
| Pytest                | Tests automatisés           |
| GitHub Actions        | Intégration continue        |

## 4. Architecture et organisation

Le système suit le fonctionnement général d'une architecture RAG :

1. Chargement et préparation des documents.
2. Découpage du corpus en chunks.
3. Génération des embeddings.
4. Stockage dans ChromaDB.
5. Recherche des passages pertinents.
6. Génération d'une réponse à partir du contexte récupéré.

Principaux dossiers du projet :

```text
ModaStyle/
├── .github/workflows/   # Intégration continue
├── configs/             # Configurations RAG
├── data/                # Corpus et données préparées
├── docs/                # Documentation
├── interface/           # Application FastAPI
├── reports/             # Résultats et rapports
├── scripts/             # Scripts utilitaires
├── src/                 # Code source RAG
├── tests/               # Tests automatisés
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## 5. Évaluation et résultats

Deux configurations de découpage documentaire ont été comparées :

- Configuration A : chunks de 500 caractères, chevauchement de 100.
- Configuration B : chunks de 800 caractères, chevauchement de 120.

L'évaluation porte sur la recherche documentaire et la qualité des réponses générées.

### Résultats principaux

| Métrique     | Configuration A | Configuration B |
| ------------ | --------------: | --------------: |
| Recall\@5    |           100 % |           100 % |
| Precision\@5 |         53,75 % |         44,72 % |
| MRR          |           0,875 |          0,9167 |
| Correctness  |         76,67 % |         93,33 % |
| Faithfulness |         93,33 % |         93,33 % |
| Relevance    |            80 % |         93,33 % |
| Score global |         83,33 % |         93,33 % |

La configuration B a été retenue comme configuration par défaut en raison de ses meilleurs résultats globaux sur la génération des réponses.

## 6. Industrialisation et qualité

Le projet intègre plusieurs mécanismes d'industrialisation :

- **MLflow :** suivi des expériences et des métriques.
- **Pytest :** exécution des tests automatisés.
- **Quality Gates :** vérification des critères d'acceptation du projet.
- **GitHub Actions :** automatisation des tests et contrôles qualité.
- **SHA-256 :** vérification de l'intégrité des documents.

Lors de la dernière validation locale, les contrôles qualité ont donné :

- 14 contrôles réussis.
- 0 contrôle échoué.
- Décision finale : **ACCEPT**.

Le rapport est disponible dans `reports/quality_gate_report.json`.

## 7. Lancement de l'application

Après installation des dépendances et configuration de la clé API Groq dans le fichier `.env`, lancer l'application avec :

```bash
python -m uvicorn interface.app:app --reload
```

Accéder à l'interface depuis :

http://127.0.0.1:8000

## 8. Documentation et reproductibilité

Les procédures détaillées concernant l'installation, la configuration, la préparation du corpus, la reconstruction de la base vectorielle, les tests et l'exécution du projet sont présentées dans le document suivant :

**Consulter le dossier de reproductibilité** : docs/DOSSIER_REPRODUCTIBILITE.md

## 9. Limites et perspectives

La qualité des réponses dépend de la couverture du corpus documentaire et de la pertinence des passages récupérés.

Les principales perspectives d'amélioration sont :

- Enrichir le corpus documentaire.
- Améliorer les stratégies de recherche.
- Étendre le jeu d'évaluation.
- Renforcer le monitoring de la latence, des erreurs et des coûts.
- Améliorer continuellement les mécanismes de sécurité.

## 10. Auteur et dépôt

**Projet académique :** Industrialisation d'un assistant intelligent basé sur RAG.

**Dépôt GitHub :**
https://github.com/marouaelmrabet/ModaStyle
