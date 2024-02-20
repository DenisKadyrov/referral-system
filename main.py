from database import DataBase

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

from utils import hash_pass

app = FastAPI()
db = DataBase()

class User(BaseModel): 
    firstName: str = Field(min_length=3, max_length=10),
    lastName: str = Field(min_length=3, max_length=10)
    email: str = Field(min_length=11, max_length=30),
    password: str = Field(min_length=8, max_length=15)
 
@app.on_event("startup")
async def startup():
    pass

@app.post("/register")
async def register(user: User, ref_code: Annotated[str, Body(min_length=6, max_length=6)] = None):
    """
    route for registration, which checks the email in db, if it is not there, it registers the user.
    Also check referral code, if there is one add him as a referral for owner of referral code
    """
    hashed_pass = hash_pass(user.password)
    check_user = db.fetchone(f"SELECT EXISTS(SELECT email FROM users WHERE email=\'{user.email}\')")
    if check_user == (False,):
        db.execute(f"INSERT INTO users (first_name, last_name, email, password) VALUES (\'{user.firstName}\', \'{user.lastName}\', \'{user.email}\', \'{hashed_pass}\')")
        db.execute(f"INSERT INTO referals (id) VALUES ((SELECT id FROM users WHERE email=\'{user.email}\'))")
        db.commit()
    
        if ref_code:
            print("hre")
            refer_id = db.fetchone(f"SELECT id FROM users WHERE code=\'{ref_code}\'")[0]
            print(refer_id)
            db.execute(f"UPDATE referals SET refer={refer_id} WHERE id=(SELECT id FROM users WHERE email=\'{user.email}\')")
            db.commit()

    return "Regiser critical"
