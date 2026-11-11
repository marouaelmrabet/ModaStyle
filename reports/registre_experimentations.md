# Registre des experimentations - ModaStyle

## Objectif

Ce registre assure le suivi des experimentations realisees sur le pipeline RAG ModaStyle.
Il conserve les objectifs, configurations, jeux de questions, metriques, resultats et fichiers associes.

Les dates exactes d'execution ne sont pas renseignees dans les exports de resultats.

## EXP-001 - Comparaison des configurations de retrieval

- Phase : 6
- Objectif : comparer les configurations A et B du decoupage documentaire.
- Corpus : version 1.0
- Jeu de test : 10 questions
- Configuration A : chunk_size = 500, chunk_overlap = 100
- Configuration B : chunk_size = 800, chunk_overlap = 120
- Modele d'embeddings : paraphrase-multilingual-MiniLM-L12-v2
- Dimension des embeddings : 384

### Resultats

| Metrique | Configuration A | Configuration B |
|---|---:|---:|
| Questions avec resultat pertinent dans le top 5 | 10/10 | 10/10 |
| Hit@5 | 100 % | 100 % |
| Precision documentaire | 49.50 % | 43.67 % |
| Documents uniques moyens | 2.6 | 2.5 |
| Temps moyen (secondes) | 0.0628 | 0.0629 |

### Conclusion

Les deux configurations obtiennent un Hit@5 de 100 %.
La configuration A presente une meilleure precision documentaire.
Les temps moyens observes sont tres proches.

Fichier de resultats : `reports/experiment_retrieval.json`
Rapport associe : `reports/rapport_experimentation_phase6.md`

## EXP-002 - Evaluation du pipeline RAG

- Phase : 7
- Objectif : evaluer la qualite du retrieval et des reponses generees.
- Corpus : version 1.0
- Questions de retrieval evaluees : 12
- Questions de reponses evaluees : 15
- Configurations comparees : A et B

### Resultats du retrieval

| Metrique | Configuration A | Configuration B |
|---|---:|---:|
| Recall@5 | 100 % | 100 % |
| Precision@5 | 53.75 % | 44.72 % |
| MRR | 0.875 | 0.917 |

### Resultats de l'evaluation des reponses

| Metrique | Configuration A | Configuration B |
|---|---:|---:|
| Correctness | 76.67 % | 93.33 % |
| Faithfulness | 93.33 % | 93.33 % |
| Relevance | 80.00 % | 93.33 % |
| Score global | 83.33 % | 93.33 % |

### Conclusion

Les deux configurations obtiennent un Recall@5 de 100 %.
La configuration A presente une meilleure Precision@5.
La configuration B presente un MRR plus eleve et un meilleur score global
dans l'evaluation des reponses.

Les scores de reponses sont des resultats preliminaires issus de la grille
d'evaluation du projet. Une validation humaine complementaire reste necessaire.

Fichiers de resultats :
- `reports/evaluation_retrieval.json`
- `reports/evaluation_answer_metrics.json`
- `reports/evaluation_answers.json`

Rapport associe : `reports/rapport_evaluation_phase7.md`

## Reproductibilite et tracabilite

Pour chaque experimentation, les elements suivants sont conserves :
- La version du corpus documentaire.
- Les configurations de decoupage.
- Le modele d'embeddings.
- Le jeu de questions utilise.
- Les metriques obtenues.
- Les fichiers de resultats JSON.
- Le rapport d'analyse.

Les fichiers JSON constituent les donnees detaillees de reference.
Ce registre fournit une synthese lisible des experimentations.

## Bilan

Deux experimentations principales sont documentees :
- EXP-001 : comparaison initiale des configurations de retrieval.
- EXP-002 : evaluation du retrieval et de la qualite des reponses.

Cette organisation facilite la comparaison des configurations et la reproduction
des evaluations.
