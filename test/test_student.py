import pytest
from fastapi.testclient import TestClient

# Utilisation des imports absolus comme nous l'avons corrigé précédemment
from src.main import app
from src.data.storage import reset_data

# Initialisation du client de test
client = TestClient(app)


# Cette fonction s'exécutera automatiquement avant CHAQUE test
@pytest.fixture(autouse=True)
def reset_db_before_test():
    reset_data()


# ==========================================
# TESTS DE LECTURE (GET)
# ==========================================


def test_1_get_students_returns_200_and_array():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_2_get_students_returns_initial_students():
    response = client.get("/students")
    data = response.json()
    assert len(data) >= 5  # On vérifie qu'il y a au moins nos 5 étudiants de départ
    assert data[0]["firstName"] == "Alice"


def test_3_get_student_by_valid_id():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["firstName"] == "Alice"


def test_4_get_student_by_inexistent_id():
    response = client.get("/students/999")
    assert response.status_code == 404


def test_5_get_student_by_invalid_id_type():
    # FastAPI renvoie notre 400 personnalisé car "abc" n'est pas un entier
    response = client.get("/students/abc")
    assert response.status_code == 400


# ==========================================
# TESTS DE CRÉATION (POST)
# ==========================================


def test_6_post_valid_student():
    new_student = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "jean.valjean@example.com",
        "grade": 15.0,
        "field": "informatique",
    }
    response = client.post("/students", json=new_student)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["firstName"] == "Jean"


def test_7_post_missing_field():
    incomplete_student = {
        "firstName": "Jean",
        # lastName est manquant
        "email": "jean2@example.com",
        "grade": 15.0,
        "field": "informatique",
    }
    response = client.post("/students", json=incomplete_student)
    assert response.status_code == 400


def test_8_post_invalid_grade():
    invalid_grade_student = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "jean.valjean3@example.com",
        "grade": 25.0,  # Invalide : supérieur à 20
        "field": "informatique",
    }
    response = client.post("/students", json=invalid_grade_student)
    assert response.status_code == 400


def test_9_post_duplicate_email():
    # Email d'Alice (ID 1) qui existe déjà
    duplicate_email_student = {
        "firstName": "Clone",
        "lastName": "Alice",
        "email": "alice@example.com",
        "grade": 10.0,
        "field": "chimie",
    }
    response = client.post("/students", json=duplicate_email_student)
    assert response.status_code == 409


# ==========================================
# TESTS DE MODIFICATION (PUT)
# ==========================================


def test_10_put_valid_data():
    updated_data = {
        "firstName": "AliceModifiée",
        "lastName": "Dupont",
        "email": "alice.mod@example.com",
        "grade": 19.0,
        "field": "informatique",
    }
    response = client.put("/students/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["firstName"] == "AliceModifiée"
    assert response.json()["grade"] == 19.0


def test_11_put_inexistent_id():
    updated_data = {
        "firstName": "Fantome",
        "lastName": "Inconnu",
        "email": "fantome@example.com",
        "grade": 10.0,
        "field": "physique",
    }
    response = client.put("/students/999", json=updated_data)
    assert response.status_code == 404


# ==========================================
# TESTS DE SUPPRESSION (DELETE)
# ==========================================


def test_12_delete_valid_id():
    response = client.delete("/students/1")
    assert response.status_code == 200
    # Vérification que l'étudiant n'existe plus
    check_response = client.get("/students/1")
    assert check_response.status_code == 404


def test_13_delete_inexistent_id():
    response = client.delete("/students/999")
    assert response.status_code == 404


# ==========================================
# TESTS STATS & SEARCH (GET)
# ==========================================


def test_14_get_stats():
    response = client.get("/students/stats")
    assert response.status_code == 200
    data = response.json()
    assert "totalStudents" in data
    assert "averageGrade" in data
    assert "studentsByField" in data
    assert "bestStudent" in data


def test_15_get_search():
    # Recherche insensible à la casse d'une partie du nom (ex: Alice)
    response = client.get("/students/search?q=ali")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["firstName"] == "Alice"
