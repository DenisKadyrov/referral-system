# lib for import debugpy, platform
from database import DataBase

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()
db = DataBase()

class User(BaseModel): 
    firstName: str = Field(min_length=3, max_length=10),
    lastName: str = Field(min_length=3, max_length=10)
    email: str = Field(min_length=11, max_length=30)

 
@app.on_event("startup")
async def startup():
    pass

@app.post("/register")
async def register(user: User, ref_code: Annotated[str, Body(min_length=6, max_length=6)] = None):
    """
    route for registration, which checks the email in db, if it is not there, it registers the user.
    Also check referral code, if there is one add him as a referral for owner of referral code
    """
    check_user = db.fetchone(f"SELECT EXISTS(SELECT Email FROM users WHERE Email=\'{user.email}\')")
    if check_user == (False,):
        db.execute(f"INSERT INTO users (FirstName, LastName, Email) VALUES (\'{user.firstName}\', \'{user.lastName}\', \'{user.email}\')")
        db.commit()
        return "Register sucsessfully"
    
    if not ref_conde:
        refer_id = db.fetchone(f"SELECT id FROM users WHERE Code=\'{ref_code}\'")[0]
        

    return "critical"
