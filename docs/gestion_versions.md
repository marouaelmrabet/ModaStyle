# Gestion des versions - ModaStyle

## 1. Objectif

Cette politique definit les regles de versionnement et de tracabilite des documents, des configurations et des traitements du projet ModaStyle.

L'objectif est de garantir la reproductibilite des experimentations et de conserver un historique des modifications.

## 2. Versionnement des documents

Les documents sources sont conserves dans `data/raw/`.

Chaque document possede :
- Un identifiant unique (MS-DOC-001 a MS-DOC-007).
- Un nom de fichier.
- Un numero de version.
- Une empreinte SHA-256 du fichier source.

La version initiale des documents est 1.0.

Regles d'evolution :
- Version majeure (2.0) : modification importante du contenu ou de la structure.
- Version mineure (1.1) : ajout ou modification d'informations.
- Correction (1.0.1) : correction mineure sans changement fonctionnel.

## 3. Integrite et tracabilite

Le fichier `data/processed/manifest.json` constitue le registre du corpus.

Il conserve notamment :
- L'identifiant de chaque document.
- Sa version.
- Son chemin source.
- Son empreinte SHA-256 originale.
- Son empreinte SHA-256 apres traitement.
- Son statut de validation.

Ces empreintes permettent de detecter toute modification du contenu.

## 4. Versionnement des configurations

Les configurations sont conservees dans `configs/`.

Le fichier `configs/rag_config.yaml` centralise :
- Les parametres de decoupage des documents.
- Les modeles d'embeddings.
- Les dimensions vectorielles.
- Les parametres de la base vectorielle.

Les modifications sont suivies avec Git afin de conserver l'historique des configurations utilisees.

## 5. Gestion des versions avec Git

Git est utilise pour suivre les documents, les configurations, le code source, les tests et les rapports.

Chaque modification importante est enregistree dans un commit avec un message explicite.

Exemples :
- Ajout des documents du corpus.
- Modification de la configuration RAG.
- Phase 8: add automated tests.

Les commits permettent de retrouver les etats precedents du projet.

## 6. Reproductibilite

Pour reproduire une experimentation, il faut conserver :
- La version du corpus.
- Le manifeste et les empreintes SHA-256.
- La configuration RAG utilisee.
- Les parametres de decoupage.
- Le modele d'embeddings.
- Les resultats et rapports de l'experimentation.

Les fichiers de resultats sont conserves dans `reports/` et les donnees de traitement dans `data/processed/`.

## 7. Conclusion

ModaStyle utilise Git pour l'historique des modifications, un manifeste JSON pour la tracabilite documentaire et SHA-256 pour controler l'integrite des documents.

Cette organisation permet de suivre les evolutions du corpus et des configurations et de faciliter la reproductibilite des experimentations.
