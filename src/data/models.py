from typing import Literal

from pydantic import BaseModel, EmailStr, Field

# Les 4 filières autorisées
FieldType = Literal["informatique", "mathématiques", "physique", "chimie"]


class StudentBase(BaseModel):
    firstName: str = Field(..., min_length=2, description="Prénom de l'étudiant (min 2 caractères)")
    lastName: str = Field(..., min_length=2, description="Nom de l'étudiant (min 2 caractères)")
    email: EmailStr = Field(..., description="Email valide et unique")
    grade: float = Field(..., ge=0, le=20, description="Note entre 0 et 20")
    field: FieldType = Field(..., description="Filière d'étude")


class Student(StudentBase):
    id: int
