# entity.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4, UUID

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1)

class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    completed: bool = False
    project_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

# repository.py
class InMemoryRepository:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.tasks = {}

    def add_user(self, user: User):
        self.users[user.id] = user
        return user

    def get_user(self, user_id: UUID):
        return self.users.get(user_id)

    def list_users(self):
        return list(self.users.values())

    def add_project(self, project: Project):
        self.projects[project.id] = project
        return project

    def get_project(self, project_id: UUID):
        return self.projects.get(project_id)

    def list_projects(self):
        return list(self.projects.values())

    def add_task(self, task: Task):
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: UUID):
        return self.tasks.get(task_id)

    def list_tasks(self):
        return list(self.tasks.values())

    def list_tasks_by_project(self, project_id: UUID):
        return [t for t in self.tasks.values() if t.project_id == project_id]

    def list_tasks_by_user(self, user_id: UUID):
        return [t for t in self.tasks.values() if t.user_id == user_id]

    def update_task_status(self, task_id: UUID, completed: bool):
        task = self.tasks.get(task_id)
        if task:
            task.completed = completed
        return task

# main.py
from fastapi import FastAPI, HTTPException
from uuid import UUID

app = FastAPI()
repo = InMemoryRepository()

@app.post("/users")
def create_user(user: User):
    return repo.add_user(user)

@app.get("/users")
def get_users():
    return repo.list_users()

@app.post("/projects")
def create_project(project: Project):
    return repo.add_project(project)

@app.get("/projects")
def get_projects():
    return repo.list_projects()

@app.post("/tasks")
def create_task(task: Task):
    if task.project_id and not repo.get_project(task.project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    if task.user_id and not repo.get_user(task.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return repo.add_task(task)

@app.get("/tasks")
def get_tasks():
    return repo.list_tasks()

@app.get("/tasks/project/{project_id}")
def get_tasks_by_project(project_id: UUID):
    return repo.list_tasks_by_project(project_id)

@app.get("/tasks/user/{user_id}")
def get_tasks_by_user(user_id: UUID):
    return repo.list_tasks_by_user(user_id)

@app.get("/tasks/{task_id}")
def get_task(task_id: UUID):
    task = repo.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}/complete")
def mark_task_complete(task_id: UUID, completed: bool):
    task = repo.update_task_status(task_id, completed)
    if nottask:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

