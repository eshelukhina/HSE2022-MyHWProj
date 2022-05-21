from concurrent.futures import ProcessPoolExecutor

import uvicorn
from fastapi import FastAPI

from database.src.database import Model
from database.src.database import engine
from result_listener.src.result_listener import ResultListener
from runner.src.runner import Runner
from web_server.src.endpoints.homeworks import homework_router
from web_server.src.endpoints.student import student_router
from web_server.src.endpoints.submitions import submitions_router
from web_server.src.endpoints.teacher import teacher_router

Model.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(homework_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(submitions_router)


def run_runner():
    Runner().run()


def run_result_listener():
    ResultListener().run()


if __name__ == "__main__":
    num_of_runners = 2

    with ProcessPoolExecutor(max_workers=num_of_runners + 1) as executor:
        for i in range(num_of_runners):
            executor.submit(run_runner)

        executor.submit(run_result_listener)

        uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
