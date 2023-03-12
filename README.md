# Créer une API sécurisée RESTFUL en utilisant Django REST / OC_p10
---------------------------------------------------------------


## TABLE DES MATIERES
---------------------

* Introduction
* Installation
* Utilisation
* Rapport Flake8


## INTRODUCTION
----------------

Ce projet consite à créer une API sécurisée RESTFUL pour le suivi des problèmes pour 3 plateformes(site web, applications Android et IOS). 
L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.
Les trois applications exploiteront les points de terminaison d'API qui serviront les données.

Principales fonctionnalités de l'application :
* Authentification des utilisateurs (inscription/connexion)
* Concernant les objets de type projet, les utilisateurs doivent avoir accès aux actions basiques de type CRUD (de l'anglais Create, Read, Update, Delete, signifiant “créer, lire, actualiser, supprimer”) sur des projets. Chaque projet doit avoir un titre, une description, un type (back-end, front-end, iOS ou Android), et un author_user_id.
* Chaque projet peut se voir associer des problèmes qui lui sont liés ; l'utilisateur ne doit pouvoir appliquer le processus CRUD aux problèmes du projet que si il ou elle figure sur la liste des contributeurs.
* Chaque problème doit avoir un titre, une description, un assigné (l’assigné par défaut étant l'auteur lui-même), une priorité (FAIBLE, MOYENNE ou ÉLEVÉE), une balise (BUG, AMÉLIORATION ou TÂCHE), un statut (À faire, En cours ou Terminé), le project_id auquel il est lié et un created_time (horodatage), ainsi que d'autres attributs mentionnés dans le diagramme de classe.
* Les problèmes peuvent faire l'objet de commentaires de la part des contributeurs au projet auquel ces problèmes appartiennent. Chaque commentaire doit être assorti d'une description, d'un author_user_id, d'un issue_id, et d'un comment_id.
* Il est interdit à tout utilisateur autorisé autre que l'auteur d'émettre des requêtes d'actualisation et de suppression d'un problème/projet/commentaire.

## INSTALLATION
------------------

* Télécharger python 3.7 (https://www.python.org/downloads/)
* Installer python 3 
* Sous Window:
    Ouvrir l'invite de commande : ``` touche windows + r``` et entrez ```cmd```
* Sous MacOs:
    Ouvrir l'invite de commande : ```touche command + espace``` et entrez ```terminal```
* Sous Linux:
    Ouvrir l'invite de commande : ```Ctrl + Alt + T```
* Mettre pip en version 21.3.1
```bash
python -m pip install --upgrade pip 21.3.1
```

* Il est préférable d'utiliser un environnement virtuel, pour l'installer:  
```bash
pip install venv
```

* Créer un dossier au nom de l'application avec mkdir
```bash
mkdir/SoftDesk
```

* Aller dans le dossier crée:
```bash
cd/SoftDesk
```

**LINUX MACOS**
* Créer votre environnement virtuel:
```bash
python3.xx -m venv .env
```
* Sourcer l'environnement virtuel:
```bash
source env/bin/activate
```

* Installer la configuration à l'aide du fichier requirements.txt:
```bash
pip install -r requirement.txt
```
**WINDOWS**
* Créer votre environnement virtuel:
```bash
python -m venv env
```
* Sourcer cette environnement virtuel:  
```bash
source env/Scripts/activate
```
* Installer la configuration à l'aide du fichier requirements.txt:
```bash
pip install -r requirement.txt
```
* Télécharger les fichiers et les dossier du repository.
* Ajouter les dans le dossier LITReview


## Utilisation 

* Naviguer dans le dossier SoftDesk et entrez la commande suivante dans le terminal pour lancer le serveur :
```bash
python manage.py runserver
```


Afin de tester les différentes fonctionalités du site, 3 comptes utilisateurs ont été créés : "jean.delacour@example.com", "paul.cour@example.com" et "francois.laporte@example.com".  
Le mot de passe est identique pour les 3 : mypassword 

#	Point de terminaison d'API	 Méthode HTTP	  URI
1.	Inscription de l'utilisateur	POST	http://127.0.0.1:8000//signup/
2.	Connexion de l'utilisateur	POST	http://127.0.0.1:8000//login/
3.	Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté	GET	http://127.0.0.1:8000//projects/
4.	Créer un projet	POST	http://127.0.0.1:8000//projects/
5.	Récupérer les détails d'un projet (project) via son id	GET	http://127.0.0.1:8000//projects/{id}/
6.	Mettre à jour un projet	PUT	http://127.0.0.1:8000//projects/{id}/
7.	Supprimer un projet et ses problèmes	DELETE	http://127.0.0.1:8000//projects/{id}/
8.	Ajouter un utilisateur (collaborateur) à un projet	POST	http://127.0.0.1:8000//projects/{id}/users/
9.	Récupérer la liste de tous les utilisateurs (users) attachés à un projet (project)	GET	http://127.0.0.1:8000//projects/{id}/users/
10.	Supprimer un utilisateur d'un projet	DELETE	http://127.0.0.1:8000//projects/{id}/users/{id}
11.	Récupérer la liste des problèmes (issues) liés à un projet (project)	GET	http://127.0.0.1:8000//projects/{id}/issues/
12.	Créer un problème dans un projet	POST	http://127.0.0.1:8000//projects/{id}/issues/
13.	Mettre à jour un problème dans un projet	PUT	http://127.0.0.1:8000//projects/{id}/issues/{id}
14.	Supprimer un problème d'un projet	DELETE	http://127.0.0.1:8000//projects/{id}/issues/{id}
15.	Créer des commentaires sur un problème	POST	http://127.0.0.1:8000//projects/{id}/issues/{id}/comments/
16.	Récupérer la liste de tous les commentaires liés à un problème (issue)	GET	http://127.0.0.1:8000//projects/{id}/issues/{id}/comments/
17.	Modifier un commentaire	PUT	http://127.0.0.1:8000//projects/{id}/issues/{id}/comments/{id}
18.	Supprimer un commentaire	DELETE	http://127.0.0.1:8000//projects/{id}/issues/{id}/comments/{id}
19.	Récupérer un commentaire (comment) via son id	GET	http://127.0.0.1:8000//projects/{id}/issues/{id}/comments/{id}



## RAPPORT FLAKE8
-------------------
* Ouvrir l'invite de commande ( se reporter à la rubrique installation)
* Lancer votre environnement virtuel ( se reporter à la rubrique installation)
* Rentrer le code suivant:
```bash
flake8 --exclude=.env/ --max-line-length=119 --format=html --htmldir=flake8-rapport
``` 
* Aller dans le dossier flake8-rapport
* Ouvrir le fichier index
