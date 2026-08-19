import os
from supabase import create_client, client
from dotenv import load_dotenv
from fastapi import Depends
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

def supabase_login(cred: credi)