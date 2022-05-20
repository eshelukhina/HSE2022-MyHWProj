import uvicorn
from fastapi import FastAPI

from src.db.database import engine
from src.db.tables import Model
from src.endpoints.homeworks import homework_router
from src.endpoints.student import student_router
from src.endpoints.submitions import submitions_router
from src.endpoints.teacher import teacher_router

Model.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(homework_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(submitions_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
