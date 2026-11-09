\# Cadrage métier — Projet ModaStyle



\## 1. Présentation du projet



ModaStyle est une boutique fictive de commerce électronique spécialisée dans la vente de vêtements et d'accessoires de mode au Maroc.



Le projet consiste à développer un assistant conversationnel intelligent basé sur l'architecture RAG (\*Retrieval-Augmented Generation\*). Cet assistant a pour objectif d'aider les clients en répondant à leurs questions à partir des documents de référence de la boutique.



L'assistant devra fournir des réponses fiables, pertinentes et accompagnées de références aux documents utilisés.



\## 2. Identification des utilisateurs



L'assistant ModaStyle s'adresse principalement à deux catégories d'utilisateurs :



\- \*\*Les clients finaux :\*\* ils souhaitent obtenir rapidement des informations concernant les produits, les commandes, les délais de livraison, les retours, les remboursements et les moyens de paiement.

\- \*\*L'équipe du support client :\*\* elle peut utiliser l'assistant pour faciliter le traitement des questions fréquentes et consulter les réponses accompagnées de leurs sources documentaires.



\## 3. Questions auxquelles l'assistant doit répondre



L'assistant doit répondre aux questions liées aux activités et aux services de ModaStyle, notamment :



\- \*\*Produits :\*\* Quels types de vêtements et d'accessoires propose ModaStyle ? Quels sont les prix des produits ?

\- \*\*Livraison :\*\* Quels sont les délais de livraison au Maroc ? Quelles sont les zones desservies ? Quels sont les frais de livraison ?

\- \*\*Retours et remboursements :\*\* Quel est le délai autorisé pour retourner un article ? Quelles sont les conditions de retour, d'échange et de remboursement ?

\- \*\*Paiements :\*\* Quels sont les moyens de paiement acceptés par ModaStyle ?

\- \*\*Tailles :\*\* Comment choisir la bonne taille ? Où trouver le guide des tailles ?

\- \*\*Entretien :\*\* Comment laver et entretenir les vêtements achetés ?



Les réponses doivent être fondées sur les informations disponibles dans les documents de référence de ModaStyle.



Si une information n'est pas présente dans la documentation, l'assistant doit le signaler clairement au lieu de produire une réponse inventée.



\## 4. Questions hors périmètre



L'assistant n'est pas destiné à traiter toutes les demandes des utilisateurs. Certaines questions et opérations sont exclues de son périmètre :



\- \*\*Modification des commandes :\*\* modifier ou annuler directement une commande en cours de livraison.

\- \*\*Opérations transactionnelles :\*\* effectuer un paiement, un remboursement ou une modification dans la base de données de la boutique.

\- \*\*Informations personnelles :\*\* consulter les comptes clients, les mots de passe ou les données personnelles.

\- \*\*Questions sans rapport avec ModaStyle :\*\* répondre à des questions générales sans lien avec la mode ou les services de la boutique.

\- \*\*Instructions malveillantes :\*\* suivre des instructions visant à contourner les règles de l'assistant, à révéler ses instructions internes ou à manipuler son comportement (\*Prompt Injection\*).



Dans ces situations, l'assistant doit refuser poliment la demande ou orienter le client vers le support humain lorsque cela est nécessaire.



\## 5. Conséquences d'une réponse incorrecte



Une réponse incorrecte ou inventée peut avoir plusieurs conséquences pour ModaStyle et ses clients :



\- \*\*Erreur sur les prix :\*\* un client peut recevoir un prix incorrect et être induit en erreur au moment de son achat.

\- \*\*Erreur sur la livraison :\*\* un client peut être informé d'un délai ou de frais de livraison inexacts.

\- \*\*Erreur sur les retours et remboursements :\*\* un client peut recevoir de fausses informations concernant ses droits ou les conditions de retour, ce qui peut entraîner un litige commercial.

\- \*\*Erreur sur les produits et les tailles :\*\* un client peut acheter un article qui ne correspond pas à ses attentes.

\- \*\*Perte de confiance :\*\* des réponses répétitivement incorrectes peuvent nuire à l'image et à la réputation de ModaStyle.



Pour limiter ces risques, l'assistant doit s'appuyer sur les documents de référence récupérés par le système RAG, fournir des références vérifiables et reconnaître ses limites.



Lorsqu'il ne trouve pas suffisamment d'informations pour répondre, il doit indiquer :



« Je ne dispose pas de cette information dans la documentation de ModaStyle. Veuillez contacter notre service client pour obtenir davantage de précisions. »



\## Conclusion



Le projet ModaStyle vise à développer un assistant RAG capable d'améliorer le support client en fournissant des réponses pertinentes et vérifiables à partir d'une base documentaire.



La fiabilité des réponses constitue une priorité : l'assistant ne doit pas inventer d'informations et doit reconnaître les questions qui dépassent son périmètre.

