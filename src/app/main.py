from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from ..routes import students
from ..data.storage import reset_data

app = FastAPI(title="Students API", description="API de gestion d'étudiants en mémoire")

# Forcer le code 400 (au lieu de 422 par défaut dans FastAPI) pour les erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Données invalides. Veuillez vérifier le format de votre requête.", "errors": exc.errors()}
    )

# Intégration du routeur
app.include_router(students.router)

# Route utilitaire (bonus) pour réinitialiser la base de données lors des tests
@app.post("/reset", tags=["Tests"])
def reset_database():
    reset_data()
    return {"message": "Base de données réinitialisée à son état d'origine."}