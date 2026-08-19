import os
from supabase import create_client, client
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

security = HTTPBearer()

load_dotenv()


class signupBody(BaseModel):
    email: str = Field(min_length=2)
    password: str = Field(min_length=8)

SUPABASE_URL= os.getenv("SUPABASE_URL")
SUPABASE_KEY= os.getenv("SUPABASE_KEY")

supabase : client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

def supabase_signup(email: str, password: str):
    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )
    return response

def supabase_login(email: str, password: str):
    response = supabase.auth.sign_in_with_password(
    {
        "email": email,
        "password": password,
    }
    )
    return response

def get_curr_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    try:
        response = supabase.auth.get_user(token)
        if not response or not response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

        return {"user":response.user, "token":token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    

def supabase_logout(token: str):
    try:
        supabase.auth.admin.sign_out(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    