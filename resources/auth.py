
from fastapi import APIRouter, Depends, HTTPException

from . import auth_handler
from schemas.auth import AuthDetail, User, UserInDB, NewUser

router = APIRouter(prefix='/api/auth')


users = []
roles = ['Super Admin', 'Admin', 'User']
user_roles = []

@router.post('/register', status_code=201)
def register(auth_detail: NewUser):
    if any(user['username'] == auth_detail.username for user in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    if any(user['email'] == auth_detail.email for user in users):
        raise HTTPException(status_code=400, detail='Email already exists')
    if any(user['phone'] == auth_detail.phone for user in users):
        raise HTTPException(status_code=400, detail='Phone number already exists')
    hashed_password = auth_handler.get_password_hash(auth_detail.password)
    new_user = {
            'username' : auth_detail.username,
            'full_name' : auth_detail.full_name,
            'email' : auth_detail.email,
            'phone' : auth_detail.phone,
            'password' : hashed_password
        }
    users.append(new_user)
    # user = [user.index(), user['username'] == auth_detail.username for user in users]
    
    user_index = users.index(new_user)
    if user_index == 0:
        user_roles.append({
            'username': auth_detail.username,
            'role':roles[0]
        })
    else:
        user_roles.append({
            'username': auth_detail.username,
            'role':roles[2]
        })
    return auth_detail.username

@router.post('/login')
def login(auth_detail: AuthDetail):
    user = None
    for i in users:
        if i['username'] == auth_detail.username:
            user = i
            break
    if (user is None) or (not auth_handler.verify_password(auth_detail.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username or password')

    # user_role = [user['username'].index() == auth_detail.username for user in user_roles]
    user_role = {}
    for i in user_roles:
        if i['username'] == auth_detail.username:
            user_role = i
            break
    token = auth_handler.encode_token(user_role['username'], user_role['role'])
    return {'token': token}