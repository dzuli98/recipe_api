from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import database
from . import token
from sqlalchemy.orm import Session
# OAuth -> Open Authorization -> lets a user grant limited access to a resource without sharing their password.
# OAuth = Authorization framework
# Authentication -> Who are you?
# Authorization -> What are you allowed to do
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # url from which oauth will fetch the token
# token url is only for openAPI swagger documentation
# at runtime is just extracts authorization header
def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception, db)
