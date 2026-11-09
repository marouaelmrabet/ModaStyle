# Inventaire du corpus documentaire — ModaStyle

**Projet :** Assistant conversationnel RAG ModaStyle  
**Identifiant du document :** MS-INV-001  
**Version de l'inventaire :** 1.0  
**Date :** 09/11/2026  
**Emplacement du corpus :** `data/raw/`

---

## 1. Présentation du corpus

Le corpus documentaire de ModaStyle regroupe les documents de référence utilisés par l'assistant conversationnel pour répondre aux questions des clients et du service client.

Les documents sont rédigés en français et concernent les activités commerciales et les services de ModaStyle.

## 2. Liste des documents

| Identifiant | Nom du fichier | Version | Domaine |
|---|---|---|---|
| MS-DOC-001 | `presentation_boutique.md` | 1.0 | Présentation de la boutique |
| MS-DOC-002 | `catalogue_produits.md` | 1.0 | Produits et prix |
| MS-DOC-003 | `livraison.md` | 1.0 | Livraison et frais |
| MS-DOC-004 | `retours_remboursements.md` | 1.0 | Retours et remboursements |
| MS-DOC-005 | `paiements.md` | 1.0 | Moyens de paiement |
| MS-DOC-006 | `guide_tailles.md` | 1.0 | Tailles et mensurations |
| MS-DOC-007 | `entretien_produits.md` | 1.0 | Conseils d'entretien |

## 3. Caractéristiques communes

- **Format :** Markdown (`.md`).
- **Langue :** Français.
- **Type de données :** Documents textuels.
- **Source :** Documents de référence préparés pour le projet ModaStyle.
- **Emplacement initial :** `data/raw/`.

## 4. Utilisation prévue

Les documents seront utilisés pour construire un assistant RAG capable de retrouver les informations pertinentes et de produire des réponses fondées sur le corpus documentaire.

Ils feront l'objet d'un contrôle qualité, d'un nettoyage et d'une préparation avant leur ingestion dans l'index vectoriel.

Les étapes de préparation comprennent notamment :

- L'extraction du contenu textuel.
- La vérification et la normalisation des métadonnées.
- Le nettoyage des contenus.
- La conservation de la provenance des documents.
- La préparation des données pour le découpage en segments (*chunks*) et la génération des embeddings.

## 5. Traçabilité et mises à jour

Chaque document possède un identifiant unique et un numéro de version.

Toute modification importante d'un document devra être enregistrée afin de conserver la traçabilité des informations utilisées par l'assistant.

Les versions des documents sources devront être suivies afin de faciliter la reproductibilité des traitements et des évaluations du système RAG.

## 6. Limites de l'inventaire

Cet inventaire décrit la composition initiale du corpus. Il ne constitue pas encore un rapport de validation de la qualité des documents.

Les résultats des contrôles seront consignés séparément dans le rapport de contrôle qualité du corpus.