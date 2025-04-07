


**1 - Introduction**

- 1.1 - Course Overview


**2 - Le langage Script**

- 2.1 - Rappels sur le fonctionnement des transactions Bitcoin :
	- Input, output
	- Scriptsig, ScriptPubKey et autres...

- 2.2 - Le Script
	- C'est quoi ?
	- Ça ressemble à quoi ?
	- Quels sont les principaux opcodes ?
	- La stack
	- Exemple d'exécution de script P2PKH

- 2.3 - Les limites et complexités du langage Script
	- Difficile de trouver le script le plus économique pour une condition de dépense donnée ;
	- Difficile de construire un script qui implémente une composition de  scripts différents : pas d'abstractions de haut niveau ;
	- Difficile d'évaluer les limites d'un script : que permet-il de faire ? Difficulté d'analyse
	- Difficile de prévoir le cout d'un output pour un script donné
	- Difficile de prévoir si un script peut dépasser les limites d'opérations
	- Fort risque d'erreur humaine sur les script non standards + langage difficilement lisible
	- à cause de tous ces inconvénients : obstacle à l'innovation car les développeurs se limitent à quelques templates éprouvés.
	- Langage enraciné dans Bitcoin : très très difficile de le changer à la fois techniquement et politiquement. Donc -> Impasse


**3 - Comprendre Miniscript**

- 3.1 - Miniscript : la solution pour fix Script ?
	- Histoire de Miniscript : inventeurs, implémentation sur Core...
	- Vulgarisation : c'est quoi Miniscript concrètement ?

- 3.2 - Le langage de Policy
	- Comprendre la différence entre Policy et Miniscript
	- Les fonctions de base en Policy

- 3.3 - Écrire des Miniscripts
	- Quelques exemples et exercices avec schémas précis


**4 - Cas d'usages : une nouvelle ère pour la self-custody

- 4.1 - La self-custody plus sûre
	- Chemin primaire et chemin de récupération
	- decaying / expanding multisig
	- mutli level wallet
	- Inconvénient : rafraichissement des coins (en cas  frais élevés...)
	- La fin de l'arbitrage entre sécurisation et récupérabilité ?

- 4.2 - L'héritage facilité
	- Rappel des problématiques sur l'héritage
	- Comment les portefeuille utilisant Miniscript viennent résoudre cela ?
	- Quelle stratégie adopter ? (purement technique 1 + 1 timelocked pour un proche, ou l'inclure sans risque dans un processus légal avec notaire...)

- 4.3 - Prise en charge de Miniscript
	- Les logiciels : Liana, Citadel?, autres?
	- Les hardware wallets


**5 - Final part**
- 5.1 - Notes
- 5.2 - Exam
- 5.3 - Conclusion


