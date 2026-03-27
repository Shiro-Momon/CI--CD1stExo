# CI--CD1stExo
A rest api to test continious integration
# API de Gestion d'Étudiants (FastAPI)

Une API RESTful développée avec Python et **FastAPI** pour gérer une base de données d'étudiants en mémoire. Ce projet inclut des opérations CRUD complètes, des statistiques, un moteur de recherche, et une suite de tests automatisés.

Ce projet a été réalisé dans le cadre d'un pipeline d'intégration et de déploiement continus (CI/CD).

## Fonctionnalités

- **CRUD complet** : Création, lecture, mise à jour et suppression d'étudiants.
- **Validation stricte** : Vérification des types, des emails (uniques et valides), et des notes (entre 0 et 20) via Pydantic.
- **Statistiques** : Endpoint dédié pour obtenir la moyenne générale, le meilleur étudiant et la répartition par filière.
- **Recherche** : Filtrage des étudiants par nom ou prénom.
- **Stockage en mémoire** : Les données sont stockées dans une liste Python et réinitialisées à chaque redémarrage (aucune base de données externe requise).

## Stack Technique

- **Framework Web** : [FastAPI](https://fastapi.tiangolo.com/)
- **Serveur ASGI** : [Uvicorn](https://www.uvicorn.org/)
- **Validation des données** : [Pydantic](https://docs.pydantic.dev/)
- **Tests automatisés** : [Pytest](https://docs.pytest.org/) & HTTPX

## Structure du Projet

```text
votre-projet/
├── src/
│   ├── __init__.py
│   ├── main.py          # Point d'entrée de l'application FastAPI
│   ├── data/
│   │   ├── __init__.py
│   │   ├── models.py    # Modèles Pydantic (Student, StudentBase)
│   │   └── store.py     # Base de données en mémoire et données initiales
│   └── routes/
│       ├── __init__.py
│       └── student.py   # Définition des endpoints API (/students)
├── tests/
│   ├── __init__.py
│   └── test_student.py  # Suite des 15 tests automatisés
├── requirements.txt     # Dépendances du projet
└── README.md

Installation
Cloner le dépôt (ou naviguer dans le dossier du projet) :

Bash
cd chemin/vers/le/projet
Créer et activer un environnement virtuel (Recommandé) :

Bash
python -m venv .venv
# Sur Windows :
.venv\Scripts\activate
# Sur macOS/Linux :
source .venv/bin/activate
Installer les dépendances :
Assurez-vous d'avoir un fichier requirements.txt contenant fastapi, uvicorn, pydantic[email], pytest, et httpx.

Bash
pip install -r requirements.txt
Démarrer le Serveur
Pour lancer l'API en mode développement avec le rechargement automatique, utilisez la commande suivante depuis la racine du projet :

Bash
python -m uvicorn src.main:app --reload
L'API sera accessible à l'adresse : http://127.0.0.1:8000

Documentation Interactive
FastAPI génère automatiquement une documentation interactive (Swagger UI). Une fois le serveur lancé, visitez :
https://www.google.com/search?q=http://127.0.0.1:8000/docs

Lancer les Tests
Le projet inclut une suite de 15 tests automatisés couvrant les cas nominaux et les erreurs (400, 404, 409).
Pour exécuter les tests, assurez-vous d'être à la racine du projet et lancez :

Bash
python -m pytest