from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session, select
from .database import tasks, create_db_tables, engine




class PostBody(BaseModel):
    title: str

class UpdateBody(BaseModel):
    title: Optional[str]
    done: Optional[bool]


app = FastAPI()

@app.get("/", description="Welcome the user")
def root_info():
    
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", description="Check if server is working")
def get_health():
    return { "status": "ok" }


@app.get("/tasks", description="Display all the tasks stored in the app")
def get_all_tasks():
    with Session(engine) as session:
        statement = select(tasks)
        tasks = session.exec(statement).all

    return tasks

@app.get("/tasks/{id}", description="Display the task based on ID")
def get_by_id(id: int):
    for task in tasks:
        if task["id"]==id:
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= f"Task {id} not found"
    )

@app.post("/tasks", description="Add a new task to the app", status_code=status.HTTP_201_CREATED)
def add_task(body: PostBody):
  ids = [task["id"] for task in tasks]
  newid = max(ids)+1
  if body.title is None or body.title=="" or body.title=="string":
     raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="No title provided or just 'string'"
     )

  else:
      newbody: dict ={
         "id": newid, "title" : body.title, "done": False
      }
      tasks.append(newbody)
      return newbody
  

@app.put("/tasks/{id}", description="Update the existing tasking based on ID")
def update_task(id: int, body: UpdateBody):
    
    if not body.model_dump(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no content in body")

    for task in tasks:
        if task["id"]==id:
            task.update(body.model_dump(exclude_unset=True))
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task of id {id} not found"

    )  




@app.delete("/tasks/{id}",description="Remove a task from app based on ID", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task of id {id} not found"
    )

