import time
from concurrent.futures import ProcessPoolExecutor

import uvicorn
from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from config import num_of_runners
from database.src.database import engine
from database.src.tables import Model
from runner.src.runner import Runner
from web_server.src.endpoints.homeworks import homework_router
from web_server.src.endpoints.student import student_router
from web_server.src.endpoints.submissions import submissions_router
from web_server.src.endpoints.teacher import teacher_router

Model.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(homework_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(submissions_router)


def run_runner():
    Runner().run()


templates = Jinja2Templates(directory="interface")


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Начальная страница", "body": "root"})


if __name__ == "__main__":
    time.sleep(30)
    with ProcessPoolExecutor(max_workers=num_of_runners + 1) as executor:
        for i in range(num_of_runners):
            executor.submit(run_runner)
        uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=False)
