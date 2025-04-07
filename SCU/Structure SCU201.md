


**1 - Introduction** 

- 1.1 - Course Overview

- 1.2 - Rappel des bases
	- Ici l'idée c'est de faire un gros recap de chaque section de SCU101 pour avoir un cours dans la continuité.


**2 - Du clic au terminal : maîtriser Linux**

- 2.1 - Le système d'exploitation : 
	- qu'est-ce que c'est, son rôle, 
	- Linux, Windows et MacOS : présentation + avantages et inconvénients

- 2.2 - L'histoire de Linux :
	- unix, GNU, Linus Torvald, open-source... 
	- (+ culture et philosophie du logiciel libre?)

- 2.3 - Les distributions GNU Linux : 
	- Debian / Red Hat / Arch Linux / Slackware / Gentoo / Autres?

- 2.4 - L'environnement de bureau : 
	- gnome, kde...

- 2.5 - Les bases pour bien débuter sur Debian : 
	- configuration, gestion de paquets, màj, firewall, utilisation terminal commandes de base, installation logiciels (browser, emails, bureautique, vlc, inkscape/gimp, dev?), connexion internet
	- bonnes pratiques


**3 - Sécuriser son ordinateur** 

- 3.1 - Accès et authentification
	- Mot de passe, BIOS
	- Cloisonnement des usages : multisession + gestion du compte root/admin
	- Création de VM
	- Le sandboxing

- 3.2 - Mises à jour
	- Mise à jour OS : expliquer comment le faire et pourquoi ?
	- Mise à jour logiciel : sur chaque système comment le faire (équivalent windows winget upgrade --all) + Lesquels sont les plus sensibles ?
	- Désinstallation des logiciels inutilisés > réduction surface d'attaque.
	- Surveillance et audit système?

- 3.3 - Signature numérique et vérification d’intégrité
	- Comment vérifier un logiciel avant de l'installer ? à quoi ça sert ? ...

- 3.4 - Chiffrement et protection des données
	- Backups
	- LUKS - Linux
	- VeraCrypt - Windows + support externes
	- Chiffrement de fichiers (GPG, Cryptomator)
	- Nettoyage des métadonnées (exiftool)

- 3.5 - Rappel des bonnes pratiques à suivre


**4 - Le navigateur : un OS dans l'OS**

- 4.1 - Brève histoire des navigateurs : 
	- les débuts du web > Mosaic, Netscape, Internet explorer > Mozilla, Safari > Domination de Chrome > avenir ?
	- Les moteurs de rendu : Trident, Gecko > KHTML, WebKit > Blink (+ chromium), EdgeHTML + parler de la domination de Blink et des difficultés pour Gecko.

- 4.2 - Le choix du navigateur (desktop only) : 
	- Chrome, Edge, Firefox, Opera, Vivaldi, Brave, Tor, Lynx, Arc.

- 4.3 - Configurer son navigateur :
	- télémétrie, cookies, https, protection renforcée, pubs, accès au périphériques, notif push...
	- + les extensions intéressantes

- 4.4 - Les bonnes pratiques : 
	- gestion des onglets, gestion des favoris, màj, "nettoyer", gestion extensions, navigation privée (explication), cloisonnement des usages.


**5 - Reprendre le contrôle de son téléphone** 

- 5.1 - Les systèmes d'exploitation mobiles :
	- Android histoire + open-source VS. Google
	- iOS histoire
	- Les alternatives open-source : Calyx, Graphene, autres?
	- Comparaison avantages/inconvénients

- 5.2 - Les bonne pratiques de sécurité
	- Màj OS + apps
	- Restriction autorisations
	- Accès et authentification (partie sur comparaison des systèmes de déverrouillage)
	- Cloisonnement (Shelter + Work Profile Andorid)

- 5.3 - Sécuriser ses communications :
	- Les apps de messagerie : comparaison + la quelle choisir pour quel usage ?
	- Une partie sur les SMS, le fonctionnement et les risques ?

- 5.4 - Remplacer ses applications :
	- Quelles apps open-source existent pour remplacer les principales app utiles : Firefox, Organic Maps, FairEmail, Etar, Nextcloud... etc (faire des recherches supplémentaires).


**6 - Sécuriser son réseau local**

- 6.1 - Comprendre son réseau local
	- Les grandes définitions pour comprendre comment ça fonctionne en restant général et haut niveau : internet, box, wi-fi, réseau local.
	- Routeur, ip locale, les ports...

- 6.2 - Sécuriser sa box / son routeur Wi-Fi
	- Changement de mot de passe + importance ;
	- Choix du type de chiffrement ;
	- Les options à désactiver.

- 6.3 - Les bonnes pratiques
	- Màj firmware ;
	- Contrôle et surveillance des appareils connectés (outils, logiciels + tuto?) ;
	- Réseau invité isolé ;
	- + pratiques avancées (installation routeur libre, cloisonner en vlan, installer un VPN niveau routeur?) - à voir, pas sûr que ce soit utile et applicable mondialement.


**7 - Partie finale** 
- 7.1 - Note
- 7.2 - Exam
- 7.3 - Conclusion