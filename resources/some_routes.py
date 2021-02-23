from fastapi import APIRouter, Depends
from . import auth_handler

router = APIRouter()


@router.get('/unprotected')
def unprotected():
    return {'message':'unprotected route'}

@router.get('/protected')
def protected(identity=Depends(auth_handler.auth_wrapper)):
    return identity