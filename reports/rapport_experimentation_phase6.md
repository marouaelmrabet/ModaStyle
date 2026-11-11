\# Phase 6 — Expérimentation et comparaison des configurations RAG



\## 1. Objectif



L'objectif de cette expérimentation est de comparer deux configurations du système RAG ModaStyle afin d'étudier l'influence des paramètres de découpage des documents sur la récupération des informations.



\## 2. Configurations comparées



| Paramètre | Configuration A | Configuration B |

|---|---:|---:|

| Taille des chunks | 500 | 800 |

| Overlap | 100 | 120 |

| Nombre de chunks | 67 | 37 |

| Modèle d'embedding | MiniLM multilingue | MiniLM multilingue |

| Top K | 5 | 5 |

| Base vectorielle | ChromaDB | ChromaDB |



Les deux configurations utilisent le même corpus, le même modèle d'embedding et les mêmes paramètres de recherche. Les paramètres de taille et d'overlap des chunks varient simultanément.



\## 3. Jeu de données de test



Un jeu de dix questions a été préparé. Les questions couvrent les domaines suivants :



\- Livraison

\- Retours et remboursements

\- Moyens de paiement

\- Guide des tailles

\- Catalogue des produits

\- Entretien des produits

\- Présentation de la boutique



Chaque question possède un document de référence attendu afin de vérifier la pertinence de la récupération.



\## 4. Métriques utilisées



\*\*Hit@5 :\*\* mesure si au moins un document attendu apparaît parmi les cinq chunks récupérés.



\*\*Précision documentaire :\*\* mesure, pour chaque question, la proportion de documents distincts récupérés qui correspondent aux documents attendus. La valeur finale est la moyenne des précisions calculées sur les questions.



\*\*Temps moyen :\*\* mesure le temps moyen consacré à la recherche et à l'encodage de la question.



\*\*Nombre moyen de documents distincts :\*\* mesure le nombre moyen de documents différents retrouvés par question.



\## 5. Résultats



| Mesure | Configuration A | Configuration B |

|---|---:|---:|

| Hit@5 | 100 % | 100 % |

| Précision documentaire | 49,5 % | 43,7 % |

| Documents distincts moyens | 2,60 | 2,50 |

| Temps moyen | 0,063 s | 0,063 s |



\## 6. Analyse



Les deux configurations obtiennent un Hit@5 de 100 %, ce qui signifie que le document attendu a été retrouvé pour chacune des dix questions.



La configuration A obtient une précision documentaire de 49,5 %, supérieure aux 43,7 % de la configuration B. Elle présente donc une meilleure précision documentaire sur le jeu de test utilisé.



La configuration B génère moins de chunks : 37 contre 67 pour A. Elle permet donc d'obtenir un index plus compact.



Les deux configurations présentent le même temps moyen mesuré de 0,063 seconde. Cette mesure, effectuée sur une seule exécution, ne permet pas de conclure à une différence de performance temporelle.



\## 7. Limites de l'expérimentation



Cette expérimentation comporte certaines limites :



\- Le jeu de test contient seulement dix questions.

\- Les paramètres de taille et d'overlap varient simultanément.

\- Les temps de réponse peuvent varier selon les conditions d'exécution.

\- Le Hit@5 ne mesure pas la qualité de la réponse générée par le modèle.

\- La précision documentaire utilisée est une mesure personnalisée au niveau des documents distincts, et non une précision classique calculée au niveau des chunks.



\## 8. Conclusion



Les résultats montrent que les deux configurations permettent de retrouver les documents attendus sur notre jeu de test.



La configuration A obtient une meilleure précision documentaire, tandis que la configuration B produit moins de chunks.



Pour cette expérimentation, la configuration A semble préférable si l'objectif prioritaire est la pertinence documentaire. La configuration B reste intéressante pour réduire le nombre de chunks dans l'index.



Une évaluation plus large sera nécessaire pour confirmer ces observations.

