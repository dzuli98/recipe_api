from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from .. hashing import Hash
import os
from datetime import timedelta

router = APIRouter(prefix="/login",
                   tags=["Authentication"])

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials!')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password!')
    # generate jwt token and return it
    # A JWT(JSON WEB TOKEN) access token is a short-lived digital key that proves
    # a user is authenticated and allowed to access protected API endpoints. 
    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
