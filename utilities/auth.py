import os

import jwt
from fastapi import HTTPException, Security
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

    def get_password_hash(self, password:str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password:str, hashed_password:str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username:str, privileges:str):
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

        return jwt.encode(payload, self.secret, algorithm=ALGORITHM)

    def decode_token(self, token:str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            print(f'============================== \\n Auth Error: {e} \\n ==============================')
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth:HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
