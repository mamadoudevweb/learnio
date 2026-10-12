# BAC SS 2027 — Cahier des charges de la première version

**Nature du projet :** application personnelle de préparation au Baccalauréat guinéen, Terminale Sciences Sociales (SS).  
**Utilisateur principal :** un seul élève, qui prépare à nouveau le BAC 2027.  
**Objectif de livraison :** première version utilisable en 48 heures, avec priorité aux fonctions pédagogiques essentielles.  
**Support :** PWA installable, mobile-first, optimisée pour Android et tablette.  
**IA privilégiée :** Google Gemini, via un backend sécurisé.  
**Statut des maquettes :** références de conception à interpréter, non spécifications pixel-perfect. Les données affichées dans les maquettes sont fictives.

## 1. Objectifs

Créer un outil d'étude personnel qui aide l'élève à :
- organiser ses cours, anciens sujets, exercices et corrigés ;
- étudier chaque leçon avec un professeur IA interactif et progressif ;
- s'entraîner avec assistance ou de façon autonome ;
- suivre ses erreurs et ses résultats ;
- planifier les révisions selon les difficultés et les échéances ;
- préparer les évaluations scolaires, les examens blancs et le BAC ;
- viser une moyenne de 13–14/20 au premier semestre, sans présenter cet objectif comme une garantie.

L'application doit enseigner les méthodes attendues dans le système scolaire guinéen. Les documents et consignes fournis par l'élève priment sur les réponses génériques de l'IA.

## 2. Principes de conception

- Interface en français, lisible sur téléphone et tablette.
- Navigation simple, cohérente et accessible.
- Palette de référence : bleu nuit, blanc, bleu vif, avec accents colorés par matière.
- Ne pas reproduire littéralement les erreurs textuelles éventuelles des maquettes ; corriger les libellés.
- Les valeurs, dates, pourcentages, scores et noms de chapitres figurant dans les maquettes sont illustratifs et ne doivent pas être préremplis comme de vraies données.
- L'application est personnelle : pas de système d'abonnement, de rôles multi-utilisateurs ou de fonctions communautaires dans la V1.

## 3. Matières

Prévoir les matières suivantes, modifiables si le programme officiel fourni l'exige :
1. Histoire
2. Géographie
3. Mathématiques
4. Français
5. Anglais
6. Économie
7. Philosophie

Chaque matière contient des chapitres. Chaque chapitre peut être lié à un cours, des exemples, des exercices, des sujets d'examen et des corrigés.

## 4. Fonctionnalités requises

### F1 — Tableau de bord
- Afficher les tâches de révision du jour.
- Afficher la prochaine évaluation et les rappels.
- Afficher la progression par matière et les chapitres à revoir.
- Donner un accès direct à la bibliothèque, au professeur IA et aux exercices.
- Présenter l'objectif de moyenne comme cible, séparément des résultats réellement obtenus.

### F2 — Bibliothèque personnelle
- Import manuel de fichiers PDF depuis l'appareil.
- Classer un document par matière, année (si connue), chapitre et type : cours, sujet, exercice, corrigé, autre.
- Permettre de consulter les documents importés et de modifier leurs métadonnées.
- Prévoir recherche et filtres simples.
- Les PDF sont prioritaires pour la V1. Les fichiers trop volumineux ou les PDF scannés devront afficher un message clair si l'extraction de texte échoue.
- Distinguer clairement les documents de l'utilisateur, les sources externes et les contenus générés par l'IA.

### F3 — Professeur IA interactif et progressif
- L'explication avance par petites sections, une notion à la fois.
- Pour chaque notion : définition, explication accessible, exemple détaillé, points à retenir et question de compréhension.
- L'élève peut interrompre et demander : explication plus simple, autre exemple, détail d'une étape, reformulation ou méthode alternative.
- Le contexte de la leçon et les messages de la séance doivent être conservés au moins durant la session ; conserver l'historique local si cela est faisable dans le délai.
- L'IA doit reconnaître les incertitudes et ne pas inventer de citations ou de références.
- Privilégier les documents personnels pertinents. Les recherches complémentaires doivent provenir de sources fiables et être identifiées comme externes.
- Ne pas affirmer qu'un sujet tombera au BAC : les analyses d'anciens sujets ne sont que des indications de fréquence/priorité.

### F4 — Exercices et entraînement
Deux modes :
- **Guidé :** l'IA fournit des indices graduels, puis une explication si l'élève reste bloqué.
- **Autonome :** l'élève soumet sa réponse avant de voir la correction.
- Pour les mathématiques, prévoir une zone de réponse utilisable pour les calculs et expressions. Un éditeur mathématique avancé est souhaitable mais peut être reporté si le délai ne le permet pas.
- Pour les dissertations et réponses rédigées, prévoir une zone de texte longue.
- La correction explique les étapes, les erreurs, la méthode et les points à retenir.
- Un score ne doit être calculé que si un barème ou une méthode d'évaluation explicite est défini. Pour les productions ouvertes, fournir une grille critériée et signaler que l'évaluation IA reste indicative.

### F5 — Planning adaptatif
- L'élève peut indiquer ses disponibilités et saisir manuellement les dates des contrôles.
- Générer un planning quotidien et hebdomadaire.
- Prioriser selon : échéance, importance du chapitre dans le programme, résultats récents, répétition des erreurs et temps disponible.
- Le planning proposé par l'IA doit rester modifiable manuellement.
- En cas de faible résultat, proposer une séance de renforcement et un exercice similaire.
- Ne pas supprimer silencieusement une tâche importante : expliquer les changements du planning.

### F6 — Tests et évaluations
- Test quotidien court.
- Évaluation hebdomadaire complète.
- Préparation des évaluations scolaires saisies par l'élève.
- Examens blancs avec durée et barème si disponibles.
- Historique : date, matière, chapitres, score, erreurs et recommandations.
- Distinguer les notes réelles de l'école des résultats des exercices générés et des estimations IA.

### F7 — Progression
- Vue générale et vue par matière.
- Statuts des chapitres : non commencé, en cours, à revoir, maîtrisé.
- Afficher les erreurs récurrentes et les prochaines actions recommandées.
- Les indicateurs de maîtrise doivent être calculés à partir des résultats enregistrés et de règles explicites, pas inventés par le modèle.
- Objectif de moyenne 13–14/20 visible comme objectif personnel, pas comme prédiction garantie.

### F8 — Rappels
- Permettre de programmer et modifier des rappels.
- Priorité aux rappels dans l'application et aux notifications locales PWA si le navigateur et les permissions le permettent.
- Indiquer clairement si une notification nécessite l'installation de la PWA ou une autorisation.
- Les notifications push serveur ne sont pas obligatoires pour la première version.

### F9 — Sauvegarde et export
- Enregistrer localement les préférences, tâches, résultats, métadonnées des documents et progression.
- Prévoir une exportation des données personnelles (JSON/CSV ou format simple documenté).
- Afficher un avertissement indiquant que les données stockées uniquement sur l'appareil peuvent être perdues lors de l'effacement des données du navigateur ou d'une réinstallation.
- La synchronisation cloud est facultative pour la V1 ; si ajoutée, elle doit être explicitement configurée.

## 5. Règles pédagogiques par matière

- **Mathématiques :** chaque calcul est détaillé ; justifier les transformations ; vérifier le résultat ; proposer une méthode alternative seulement si elle est correcte et acceptable dans le contexte scolaire.
- **Français / Philosophie :** analyser la consigne, définir les termes, construire problématique et plan, structurer introduction/développement/conclusion, corriger avec critères explicites.
- **Histoire / Géographie :** dates et notions vérifiables, causes/conséquences, analyse de documents, cartes ou graphiques lorsqu'ils sont fournis.
- **Économie :** définitions, mécanismes, raisonnements et exemples contextualisés.
- **Anglais :** grammaire, vocabulaire, compréhension, traduction et expression avec corrections expliquées.

L'élève fournira progressivement les programmes, méthodes de classe, sujets et corrigés. Ne pas supposer que les chapitres ou formats sont officiels avant validation des documents.

## 6. Architecture technique souhaitée

Le développeur est libre de choisir les bibliothèques exactes, mais doit respecter ces principes :
- PWA responsive, mobile-first, déployable sur Vercel.
- Backend/serverless pour toutes les requêtes Gemini.
- Clé Gemini stockée uniquement dans les variables d'environnement privées du serveur. Jamais dans le bundle client, dans le dépôt ou dans les logs.
- Valider et limiter les entrées côté serveur ; prévoir des limites de taille, de fréquence et de consommation pour éviter les abus accidentels.
- Utiliser IndexedDB pour les données structurées et volumineuses côté client ; `localStorage` seulement pour de petites préférences.
- Prévoir un service worker et un cache des ressources statiques pour ouvrir l'interface hors ligne.
- Les fonctionnalités Gemini, recherches en ligne et génération de contenu nécessitent une connexion.
- Les PDF scannés, l'OCR, l'analyse massive du corpus et les traitements multimodaux avancés peuvent nécessiter des étapes supplémentaires ; ne pas prétendre qu'ils fonctionnent si non implémentés.
- Ne pas inclure de secrets dans GitHub. Utiliser `.env.example` avec des noms de variables sans valeurs.
- Prévoir une gestion d'erreurs visible, sans exposer de détails sensibles.

## 7. Critères d'acceptation de la V1

La V1 est considérée utilisable lorsque :
1. La PWA s'ouvre correctement sur Android et peut être installée.
2. Les six écrans de référence sont reproduits dans une interface cohérente.
3. Les sept matières et une structure de chapitres sont consultables.
4. Un PDF peut être importé, classé, retrouvé et ouvert.
5. Une leçon peut être expliquée par Gemini et l'élève peut poser une question de suivi.
6. Le mode guidé propose un indice avant la solution complète ; le mode autonome permet de soumettre une réponse avant correction.
7. Une évaluation enregistre date, matière, réponses et résultat.
8. Le planning peut être modifié et les tâches terminées restent enregistrées après fermeture/réouverture.
9. La progression est calculée à partir des données réelles de l'application.
10. La clé Gemini n'est pas visible dans les fichiers du navigateur ni dans GitHub.
11. Une exportation des données fonctionne.
12. Les erreurs de réseau, d'import et d'appel IA affichent un message compréhensible.

## 8. Priorités si le délai de 48 heures devient contraignant

**P0 — indispensable :** navigation, bibliothèque PDF manuelle, matières/chapitres, leçon interactive Gemini, exercices guidés et autonomes, sauvegarde locale, planning simple, backend sécurisé.

**P1 — à intégrer si le temps le permet :** tests quotidiens/hebdomadaires, progression détaillée, rappels locaux, examens blancs chronométrés.

**P2 — après la première livraison :** OCR de PDF scannés, import massif, recherche web intégrée, analyse approfondie de tout le corpus, audio/vidéo, synchronisation cloud avancée.

Le développeur doit signaler honnêtement les fonctions non terminées plutôt que les simuler.

## 9. Sécurité et confidentialité

- L'application étant personnelle, éviter de collecter des données non nécessaires.
- Ne pas committer de clés API, tokens ou fichiers de service.
- Utiliser des variables d'environnement côté serveur.
- Ne pas envoyer tout le corpus à Gemini à chaque requête : ne transmettre que les extraits nécessaires.
- Examiner les conditions de conservation et d'utilisation des données du fournisseur IA avant de lui envoyer des documents personnels.
- Ne pas exposer publiquement les PDF importés sans décision explicite de l'utilisateur.

## 10. Documents à fournir au développeur

- `CAHIER_DES_CHARGES.md` : le présent document.
- `maquettes/01_accueil.png` à `maquettes/06_progression_resultats.png` : références visuelles.
- Les programmes officiels et les documents scolaires fournis ensuite par l'élève.
- Un fichier `README.md` décrivant comment installer, configurer et déployer le projet.

**Note importante :** les maquettes sont indicatives. Le développeur doit privilégier la lisibilité, la cohérence et le bon fonctionnement sur mobile plutôt qu'une copie exacte des images.
