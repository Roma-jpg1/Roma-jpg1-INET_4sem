from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="tasks-s18")


class Task(BaseModel):
    id: int
    due: str


class CreateTask(BaseModel):
    due: str


tasks_db: List[Task] = [
    Task(id=1, due="2026-05-20"),
    Task(id=2, due="2026-05-27"),
]

next_id = len(tasks_db) + 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db


@app.post("/tasks", response_model=Task)
def create_task(task: CreateTask):
    global next_id
    new_task = Task(id=next_id, due=task.due)
    tasks_db.append(new_task)
    next_id += 1
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
