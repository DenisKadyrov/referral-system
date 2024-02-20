from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: str | None = None
