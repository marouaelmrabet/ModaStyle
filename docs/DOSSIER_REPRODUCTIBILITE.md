# Dossier de reproductibilité — ModaStyle

**Projet :** Industrialisation d'un assistant RAG pour ModaStyle
**Version du projet :** 1.0
**Langue :** Français
**Dépôt GitHub :** https://github.com/marouaelmrabet/ModaStyle

---

## 1. Objectif du dossier

Ce dossier décrit les étapes nécessaires pour installer, configurer, reconstruire et exécuter le projet ModaStyle dans un environnement local.

Il présente également les procédures de test, d'évaluation, de suivi des expériences et de contrôle qualité afin de garantir la traçabilité et la reproductibilité du système RAG.

## 2. Environnement technique

L'environnement de développement utilisé est le suivant :

| Élément                  | Version ou technologie                |
| ------------------------ | ------------------------------------- |
| Système de développement | Windows                               |
| Python                   | 3.12.0                                |
| Gestion des dépendances  | pip                                   |
| Environnement virtuel    | venv                                  |
| Base vectorielle         | ChromaDB 1.5.9                        |
| Modèle d'embeddings      | paraphrase-multilingual-MiniLM-L12-v2 |
| Dimension des embeddings | 384                                   |
| Modèle de génération     | openai/gpt-oss-20b                    |
| Fournisseur LLM          | Groq                                  |
| Suivi des expériences    | MLflow 3.18.0                         |
| Interface                | FastAPI 0.162.5                       |
| Serveur local            | Uvicorn 0.54.0                        |

Les versions des bibliothèques Python sont définies dans les fichiers `requirements.txt` et `requirements-dev.txt`.

## 3. Récupération du projet

Cloner le dépôt GitHub :

```bash
git clone https://github.com/marouaelmrabet/ModaStyle.git
cd ModaStyle
```

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\venv\Scripts\Activate.ps1
```

Installer les dépendances principales et de développement :

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Vérifier les dépendances :

```bash
pip check
```

## 4. Configuration des variables d'environnement

Le projet utilise une clé API Groq pour accéder au modèle de génération.

Créer un fichier `.env` à la racine du projet à partir du modèle `.env.example`.

```env
GROQ_API_KEY=votre_cle_api_groq
```

Le fichier `.env` est exclu du suivi Git grâce au `.gitignore`.

## 5. Gestion et versionnement du corpus

Le corpus documentaire est stocké dans `data/raw/`.

Il comprend sept documents Markdown :

| Identifiant | Document                    |
| ----------- | --------------------------- |
| MS-DOC-001  | Présentation de la boutique |
| MS-DOC-002  | Catalogue des produits      |
| MS-DOC-003  | Livraison                   |
| MS-DOC-004  | Retours et remboursements   |
| MS-DOC-005  | Paiements                   |
| MS-DOC-006  | Guide des tailles           |
| MS-DOC-007  | Entretien des produits      |

Les documents sont versionnés avec un identifiant et un numéro de version.

Le fichier `data/processed/manifest.json` contient les informations de provenance et les empreintes SHA-256 permettant de vérifier l'intégrité des sources.

Les données sources sont conservées dans Git. Les fichiers générés et la base vectorielle locale ne sont pas versionnés.

## 6. Reconstruction du corpus et de la base vectorielle

La reconstruction de l'index suit quatre étapes.

### 6.1 Préparation du corpus

Exécuter :

```bash
python scripts/prepare_corpus.py
```

Cette étape vérifie les sept documents, leurs identifiants, leurs versions et leur contenu.

Elle produit notamment :

- `data/processed/documents_extraits.jsonl`
- `data/processed/manifest.json`
- `reports/controle_qualite_corpus.md`

### 6.2 Découpage des documents

Exécuter :

```bash
python -m src.chunking
```

Deux configurations sont générées :

| Configuration | Taille des chunks | Overlap |
| ------------- | ----------------: | ------: |
| A             |               500 |     100 |
| B             |               800 |     120 |

Les fichiers produits sont `chunks_A.jsonl` et `chunks_B.jsonl`.

### 6.3 Génération des embeddings

Exécuter :

```bash
python -m src.embeddings
```

Le modèle multilingue `paraphrase-multilingual-MiniLM-L12-v2` génère des vecteurs de dimension 384.

Les embeddings sont normalisés et enregistrés dans :

- `data/processed/embeddings_A.jsonl`
- `data/processed/embeddings_B.jsonl`

### 6.4 Stockage dans ChromaDB

Exécuter :

```bash
python -m src.vector_store
```

Les deux collections sont créées :

- `modastyle_a`
- `modastyle_b`

La métrique de distance utilisée est la similarité cosinus.

La base persistante est stockée localement dans `data/chroma_db/`.

**Important :** la reconstruction remplace les collections portant ces noms. Elle doit être effectuée uniquement lorsque cela est nécessaire.

### 6.5 Vérification de l'index

Exécuter :

```bash
python scripts/verify_vector_store.py
```

Résultat vérifié sur l'environnement de développement :

| Collection  | Chunks attendus | Chunks obtenus |
| ----------- | --------------: | -------------: |
| modastyle_a |              67 |             67 |
| modastyle_b |              37 |             37 |

Les textes et les métadonnées étaient disponibles dans les deux collections.

## 7. Exécution de l'application RAG

L'application utilise la configuration B par défaut, avec un nombre de résultats récupérés fixé à 5.

Lancer le serveur :

```bash
python -m uvicorn interface.app:app --reload
```

Ouvrir ensuite l'adresse suivante dans un navigateur :

[http://127.0.0.1:8000](http://127.0.0.1:8000)

L'application expose également :

- `GET /` : interface utilisateur.
- `POST /ask` : traitement des questions.
- `GET /health` : vérification de disponibilité.
- `GET /monitoring` : consultation des indicateurs de qualité et de performance.

Le terminal qui exécute Uvicorn doit rester ouvert pendant l'utilisation de l'application.

## 8. Tests automatisés

Les tests sont réalisés avec pytest.

Exécuter :

```bash
python -m pytest -v
```

Les tests couvrent les composants du système RAG, notamment la génération, la protection des entrées, la construction du contexte et les limites du système.

Le projet utilise également un script de quality gates.

## 9. Quality Gates

Exécuter :

```bash
python scripts/quality_gate.py
```

Les contrôles portent sur :

- Les tests automatisés.
- L'intégrité du corpus.
- La configuration RAG.
- Les performances du retrieval.
- La qualité des réponses générées.

Les seuils définis dans le script sont :

| Métrique     | Seuil minimal |
| ------------ | ------------: |
| Recall\@5    |          95 % |
| Correctness  |          75 % |
| Faithfulness |          90 % |
| Relevance    |          80 % |
| Score global |          80 % |

La décision finale est :

- **ACCEPTE** si tous les contrôles réussissent.
- **REJETE** si au moins un contrôle échoue.

Le rapport est généré dans `reports/quality_gate_report.json`.

Dernière validation locale enregistrée : **14 contrôles réussis et 0 échec**.

## 10. Suivi des expériences avec MLflow

Le projet utilise MLflow pour assurer le suivi des expériences et des métriques.

Importer les résultats des évaluations existantes :

```bash
python scripts/import_results_mlflow.py
```

L'expérience MLflow est nommée `ModaStyle_RAG`.

Le suivi utilise une base SQLite locale :

`mlflow.db`

Les artefacts sont enregistrés dans :

`mlartifacts/`

Les expériences enregistrent les paramètres des configurations A et B, les métriques de retrieval et les scores de génération.

Cette procédure importe les résultats déjà calculés ; elle ne relance pas les évaluations.

Pour consulter l'interface MLflow :

```bash
mlflow ui
```

Puis ouvrir :

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## 11. Intégration continue

Le workflow GitHub Actions est défini dans :

`.github/workflows/tests.yml`

Il se déclenche lors des événements `push` et `pull_request`.

Il utilise Ubuntu et Python 3.12, installe les dépendances de développement, exécute les tests pytest puis les quality gates.

Le résultat local validé est de 14 contrôles réussis. Le statut d'exécution distante doit être consulté dans l'onglet Actions du dépôt GitHub.

## 12. Gestion des fichiers et reproductibilité

Les fichiers sources et les configurations sont versionnés avec Git.

Les éléments suivants sont exclus du dépôt :

- `.env`
- `venv/` et `.venv/`
- `data/chroma_db/`
- `mlruns/`
- `mlflow.db`
- `mlartifacts/`
- Les caches Python et fichiers temporaires.

La base vectorielle, les expériences MLflow et les artefacts doivent donc être reconstruits localement à partir des sources et des scripts du projet.

Les fichiers d'évaluation et les rapports utiles à la traçabilité sont conservés dans `reports/`.

## 13. Limites et précautions

La reproductibilité dépend notamment :

- De la disponibilité du modèle d'embeddings et de ses dépendances.
- De la disponibilité du service Groq et de la validité de la clé API.
- De la conservation des documents sources et de leurs versions.
- De la stabilité des versions des bibliothèques utilisées.

Les réponses générées par un modèle de langage peuvent varier. Les résultats d'évaluation doivent donc être interprétés en tenant compte de cette variabilité.

---

## Monitoring et observabilité

Le projet ModaStyle intègre un système de monitoring minimal permettant de suivre les performances techniques et la qualité du système RAG.

### 1. Suivi des requêtes et des erreurs
Chaque requête est enregistrée avec son statut (succès ou erreur), sa durée de traitement et, lorsqu'ils sont disponibles, les tokens consommés. Les erreurs sont également consignées dans un journal dédié.

### 2. Suivi de la latence
Le système calcule la latence moyenne et le percentile 95 (P95), afin de suivre le temps de réponse de l'assistant.

### 3. Suivi de la consommation
Le nombre de tokens d'entrée et de sortie fournis par l'API Groq est enregistré lorsqu'il est disponible. Le coût financier n'est pas calculé automatiquement.

### 4. Suivi de la qualité RAG
Le monitoring récupère les résultats du dernier rapport `reports/quality_gate_report.json`, notamment :
- Recall@5 ;
- Correctness ;
- Faithfulness ;
- Relevance ;
- Score global.

Ces métriques sont issues de l'évaluation périodique du corpus de questions, et non d'une mesure automatique de chaque réponse en temps réel.

### 5. Accès au monitoring
Après démarrage de l'application, les indicateurs sont consultables à l'adresse :

`http://127.0.0.1:8000/monitoring`

Les journaux techniques sont stockés localement dans le dossier `logs/`, exclu du dépôt Git.

### 6. Résultat de validation
Lors de la validation du 12 novembre 2026 :
- 2 requêtes enregistrées ;
- 0 erreur ;
- latence moyenne : 1 782,29 ms ;
- latence P95 : 3 314,58 ms ;
- consommation totale : 1 261 tokens ;
- Quality Gate : 14 contrôles réussis sur 14.

Ces résultats constituent une observation de validation et non une garantie de performances futures.
**Fin du dossier de reproductibilité — ModaStyle**
