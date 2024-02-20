from database import DataBase

from fastapi import FastAPI, Body, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Annotated

from utils import hash_pass
from oauth import create_access_token, get_current_user

import schemas
import utils


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
            try:
                refer_id = db.fetchone(f"SELECT id FROM users WHERE code=\'{ref_code}\'")[0]
                db.execute(f"UPDATE referals SET refer={refer_id} WHERE id=(SELECT id FROM users WHERE email=\'{user.email}\')")
                db.commit()
            except:
                return "not code"
    return "Sucsessfull"
 

@app.post('/login', response_model=None)
async def login(userdetails: OAuth2PasswordRequestForm = Depends()):
    """
    get id and password from bd and check with userdetails name and password
    """
    user = db.fetchone(f"SELECT id, password FROM users WHERE email=\'{userdetails.username}\'")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user doesn't exist")

    if not utils.verify_password(userdetails.password, user[1]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The password in not match")

    access_token = create_access_token(data={"user_id": str(user[0])})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/create_code')
async def me(user: User = Depends(get_current_user)):
    db.execute(f"UPDATE users SET code=\'3kg5kd\' WHERE id={user['id']}")
    db.commit()
    return user
