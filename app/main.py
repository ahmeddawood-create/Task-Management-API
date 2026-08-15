from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session, select
from app.database import tasks, engine




class PostBody(BaseModel):
    title: str = Field(min_length=1)

class UpdateBody(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


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
        alltasks = session.exec(statement).all()
        return alltasks

@app.get("/tasks/{id}", description="Display the task based on ID")
def get_by_id(id: int):
    with Session(engine) as session:
        statement = select(tasks).where(tasks.id==id)
        onetask = session.exec(statement).one_or_none()
        if onetask is not None:
            return onetask
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Task {id} not found"
            )            




@app.post("/tasks", description="Add a new task to the app", status_code=status.HTTP_201_CREATED)
def add_task(body: PostBody):
    if (body.title != "string") :
        newtask = tasks(title=body.title)
        with Session(engine) as session:
            session.add(newtask)
            session.commit()
            session.refresh(newtask)

        return newtask
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No title provided or just 'string'"
    )
    



@app.put("/tasks/{id}", description="Update the existing tasking based on ID")
def update_task(id: int, body: UpdateBody):
    with Session(engine) as session:
        statement = select(tasks).where(tasks.id == id)
        onetask = session.exec(statement).first()

        if (body.title== None) and (body.done == None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no content in body")

        if onetask is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no task with this id")


        if body.title is not None:
            onetask.title = body.title


        if body.done is not None:
            onetask.done = body.done

        session.add(onetask)
        session.commit()
        session.refresh(onetask)
        return onetask
        

    


@app.delete("/tasks/{id}",description="Remove a task from app based on ID", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):

    with Session(engine) as session:
        statement = select(tasks).where(tasks.id == id)
        onetask = session.exec(statement).first()

        if onetask is not None:
            session.delete(onetask)
            session.commit()
            return {"detail":"task removed successfully"}
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no content related to this id")

