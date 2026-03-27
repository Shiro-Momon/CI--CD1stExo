from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, status

from src.data.models import Student, StudentBase
from src.data.storage import students_db

router = APIRouter(prefix="/students", tags=["Students"])


# 1. GET /students/stats (Déclaré AVANT /{id})
@router.get("/stats")
def get_stats():
    if not students_db:
        return {
            "totalStudents": 0,
            "averageGrade": 0,
            "studentsByField": {},
            "bestStudent": None,
        }

    total = len(students_db)
    avg = round(sum(s.grade for s in students_db) / total, 2)

    by_field = {}
    for s in students_db:
        by_field[s.field] = by_field.get(s.field, 0) + 1

    best = max(students_db, key=lambda s: s.grade)

    return {
        "totalStudents": total,
        "averageGrade": avg,
        "studentsByField": by_field,
        "bestStudent": best.model_dump(),
    }


# 2. GET /students/search (Déclaré AVANT /{id})
@router.get("/search")
def search_students(q: str = Query(default=None)):
    # On renvoie 400 si q est absent ou vide
    if not q or not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Le paramètre 'q' est obligatoire et ne peut pas être vide.",
        )

    q_lower = q.lower()
    results = [s for s in students_db if q_lower in s.firstName.lower() or q_lower in s.lastName.lower()]
    return results


# 3. GET /students
@router.get("", response_model=List[Student])
@router.get("/", response_model=List[Student], include_in_schema=False)
def get_all_students():
    return students_db


# 4. GET /students/{id}
@router.get("/{id}", response_model=Student)
def get_student(id: int = Path(...)):
    for s in students_db:
        if s.id == id:
            return s
    raise HTTPException(status_code=404, detail="Étudiant introuvable.")


# 5. POST /students
@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED)
@router.post(
    "/",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_student(student_in: StudentBase):
    # Vérification de l'unicité de l'email (Erreur 409)
    if any(s.email == student_in.email for s in students_db):
        raise HTTPException(status_code=409, detail="Cet email est déjà utilisé.")

    # Auto-génération de l'ID
    new_id = max((s.id for s in students_db), default=0) + 1
    new_student = Student(id=new_id, **student_in.model_dump())

    students_db.append(new_student)
    return new_student


# 6. PUT /students/{id}
@router.put("/{id}", response_model=Student)
def update_student(student_in: StudentBase, id: int = Path(...)):
    # Recherche de l'étudiant
    student_idx = next((i for i, s in enumerate(students_db) if s.id == id), None)
    if student_idx is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")

    # Vérification de l'unicité de l'email pour un AUTRE étudiant
    if any(s.email == student_in.email and s.id != id for s in students_db):
        raise HTTPException(status_code=409, detail="Cet email est déjà utilisé par un autre étudiant.")

    updated_student = Student(id=id, **student_in.model_dump())
    students_db[student_idx] = updated_student
    return updated_student


# 7. DELETE /students/{id}
@router.delete("/{id}")
def delete_student(id: int = Path(...)):
    student_idx = next((i for i, s in enumerate(students_db) if s.id == id), None)
    if student_idx is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")

    students_db.pop(student_idx)
    return {"message": f"L'étudiant avec l'ID {id} a été supprimé avec succès."}
