from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session, select
from app.database import tasks, engine
from app.supabase import signupBody, supabase_signup, supabase_login, get_curr_user, supabase_logout




class PostBody(BaseModel):
    title: str = Field(min_length=1)

class UpdateBody(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK , description="Welcome the user")
def root_info():
    
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health",status_code=status.HTTP_200_OK , description="Check if server is working")
def get_health():
    return { "status": "ok" }


@app.get("/tasks",status_code=status.HTTP_200_OK, description="Display all the tasks stored in the app")
def get_all_tasks():
    with Session(engine) as session:
        statement = select(tasks)
        alltasks = session.exec(statement).all()
        return alltasks

@app.get("/tasks/{id}",status_code=status.HTTP_200_OK , description="Display the task based on ID")
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
    



@app.put("/tasks/{id}",status_code=status.HTTP_200_OK, description="Update the existing tasking based on ID")
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

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def register_user(body: signupBody):
    try:
        response = supabase_signup(body.email, body.password)
        return {
            "message": "Successfully signed up!",
            "user_id": response.user.id,
            "email": response.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login_user(body: signupBody):
    try:
        response =supabase_login(body.email,body.password)
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.get("/public/info", status_code=status.HTTP_200_OK)
def get_public_info():
    return { "message": "Welcome stranger! This info is public." }

@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_protected_profile(curr_user = Depends(get_curr_user)):
    return {
        "message": "Welcome! It's a protected profile.",
        "user_info": curr_user
        
    }

@app.post("/auth/logout", status_code=status.HTTP_200_OK)
def logout_user(curr_user = Depends(get_curr_user)):
    supabase_logout(curr_user)
    return {"message":"Successfully logout"}