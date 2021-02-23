
from fastapi import APIRouter, Depends, HTTPException, status

from . import auth_handler
from schemas.auth import AuthDetail, User, UserInDB, NewUser

router = APIRouter(prefix='/api/auth')


users = []
roles = ['Super Admin', 'Admin', 'User']
user_roles = []

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(auth_detail: NewUser):
    if any(user['username'] == auth_detail.username for user in users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username is taken')
    if any(user['email'] == auth_detail.email for user in users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    if any(user['phone'] == auth_detail.phone for user in users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Phone number already exists')

    hashed_password = await auth_handler.get_password_hash(auth_detail.password)
    new_user = {
            'username' : auth_detail.username,
            'full_name' : auth_detail.full_name,
            'email' : auth_detail.email,
            'phone' : auth_detail.phone,
            'password' : hashed_password
        }
    users.append(new_user)
    
    user_index = users.index(new_user)

    # Create User roles
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

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(auth_detail: AuthDetail):
    user = None
    for i in users:
        if i['username'] == auth_detail.username:
            user = i
            break
    if (user is None) or (not await auth_handler.verify_password(auth_detail.password, user['password'])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    # Fetch User roles to add to token
    user_role = {}
    for i in user_roles:
        if i['username'] == auth_detail.username:
            user_role = i
            break
    token = await auth_handler.encode_token(user_role['username'], user_role['role'])
    return {'token': token}