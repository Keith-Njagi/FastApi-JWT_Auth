import os

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

# openssl rand -hex 32 ->to generate random SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = SECRET_KEY

    @classmethod
    async def get_password_hash(cls, password:str):
        return cls.pwd_context.hash(password)

    @classmethod
    async def verify_password(cls, plain_password:str, hashed_password:str):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def encode_token(cls, username:str, privileges:str):
        is_admin:bool = False
        if privileges == 'Admin' or privileges == 'Super Admin':
            is_admin = True

        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat':datetime.utcnow(),
            'sub':{ 
                'identity':{
                    'id':username,
                    'privileges':privileges,
                },
                'claims':{
                    'is_admin':is_admin
                }
            }
            
        }

        return jwt.encode(payload, cls.secret, algorithm=ALGORITHM)

    @classmethod
    def decode_token(cls, token:str):
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORISED,detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            print(f'============================== \\n Auth Error: {e} \\n ==============================')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORISED, detail='Invalid token')

    @classmethod
    def auth_wrapper(cls, auth:HTTPAuthorizationCredentials = Security(security)):
        return cls.decode_token(auth.credentials)
