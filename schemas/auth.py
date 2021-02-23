from typing import Optional

from pydantic import BaseModel

class AuthDetail(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    full_name: str = None
    email: str = None
    phone: str
    is_active: Optional[bool] = False

class UserInDB(User):
    password: str

class NewUser(User):
    password:str


class UserRole:
    username: str
    role: str