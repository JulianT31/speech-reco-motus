# Motus avec reconnaissance vocal

Projet 3A SRI UPSSITECH 2023

Auteurs : Julian TRANI & Pauline JOBERT

![Review](/assets/review_game.png)

**L'application a été implémentée et testée sous Windows**. Nous ne garantissons pas son fonctionnement sous d'autres systèmes d'exploitation tels que Linux ou MacOS.

## Installation de l'application

Pour installer l'application et de la rendre fonctionnelle, il faut :

-   Cloner le repo [https://github.com/JulianT31/speech-reco-motus](https://github.com/JulianT31/speech-reco-motus) sur votre ordinateur
-   Télécharger et déposer l'application Whiboard dans le répertoire `/speech-reco-motus`

## Setup de l'environnement des différents agents python

Au niveau de l'environnement python, nous utilisons la version 3.10. Les différents agents utilisent les libraires suivantes :

-   la version 3.6.4 de la libraire `ingescape`
-   la version 3.10.0 de `SpeechRecognition`
-   la version 0.2.13 de `PyAudio`

Pour installer toutes libraires, vous pouvez utiliser le fichier `{requirements.txt` et exécuter la commande suivante : `pip install -r requirements.txt` dans le répertoire pour installer ces libraires. Sinon, vous pouvez les installer chacune manuellement.

Pour utiliser les différents agents python (`Speech_reco` / `Motus_game`), il faut les exécuter avec l'option suivante suivante : \verb|--device Wi-Fi|

Si vous utilisez `PyCharm`, vous pouvez directement ajouter cette option dans les paramètres de configuration (Run/Debug Configurations) comme sur la figure

![Pycharm](/assets/param_pycharm.png)

## Lancement de l'application

Pour lancer correctement l'application, il faut respecter l'ordre de lancement :

-   Le Whiteboard, avec un terminal dans le répertoire courant, exécuter la commande suivante `.\Whiteboard\Whiteboard.exe --device Wi-Fi`
-   L'agent python `Speech_rec` avec l'option `--device Wi-Fi` comme expliqué précédemment
-   L'agent python `Motus_game` avec l'option `--device Wi-Fi` comme expliqué précédemment

## Utilisation de l'application

Une fois l'application lancée, pour proposer un mot par la reconnaissance vocale il faut lancer une impulsion avec `Ingescape Circle` sur l'agent `Speech_reco`. Le message _"Recording in progress. Speak now..."_ s'affiche sur la console du Whiteboard qui mentionne que l'agent écoute l'entrée audio.
Il faut répéter l'opération pour tout nouveau mot à ajouter dans le jeu.

Attention, s'il y a du bruit ambiant autour du micro, la reconnaissance ne sera pas très performante.
