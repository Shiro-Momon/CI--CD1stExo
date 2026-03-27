from typing import List

from .models import Student

# Données de test initiales
INITIAL_DATA = [
    {
        "id": 1,
        "firstName": "Alice",
        "lastName": "Dupont",
        "email": "alice@example.com",
        "grade": 15.5,
        "field": "informatique",
    },
    {
        "id": 2,
        "firstName": "Bob",
        "lastName": "Martin",
        "email": "bob@example.com",
        "grade": 12.0,
        "field": "mathématiques",
    },
    {
        "id": 3,
        "firstName": "Charlie",
        "lastName": "Durand",
        "email": "charlie@example.com",
        "grade": 18.5,
        "field": "physique",
    },
    {
        "id": 4,
        "firstName": "Diana",
        "lastName": "Leroy",
        "email": "diana@example.com",
        "grade": 9.0,
        "field": "chimie",
    },
    {
        "id": 5,
        "firstName": "Eve",
        "lastName": "Moreau",
        "email": "eve@example.com",
        "grade": 14.0,
        "field": "informatique",
    },
]

students_db: List[Student] = []


def reset_data():
    """Réinitialise la base de données en mémoire avec les valeurs par défaut."""
    global students_db
    students_db.clear()
    for s in INITIAL_DATA:
        students_db.append(Student(**s))


# Initialisation au démarrage
reset_data()
