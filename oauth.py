from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import DataBase
import schemas


db = DataBase()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "f95e9b9542d2c4e33451b88a87e4ccf53b82bb5e6d29bbe6813e2b457bae5193"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.DataToken(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_token_access(token, credentials_exception)

    user_resp = db.fetchone(f"SELECT id, first_name, last_name, email, code, password FROM users WHERE id=\'{token.id}\'")
    user = {
        'id': user_resp[0],
        'first_name': user_resp[1],
        'last_name': user_resp[2],
        'email': user_resp[3],
        'code': user_resp[4],
        'password': user_resp[5]
    }
    return user
