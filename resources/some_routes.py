from fastapi import APIRouter, Depends, status
from . import auth_handler

router = APIRouter()


@router.get('/unprotected', status_code=status.HTTP_200_OK)
async def unprotected():
    return {'message':'unprotected route'}

@router.get('/protected', status_code=status.HTTP_200_OK)
async def protected(identity=Depends(auth_handler.auth_wrapper)):
    return identity