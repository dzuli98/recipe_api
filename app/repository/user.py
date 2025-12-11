from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas


def create(request: schemas.UserCreate, db: Session):
    try:
        username  = request.username.strip().lower()
        user_obj = db.query(models.User).filter(models.User.username == username).first()
        if user_obj:
            return user_obj
        new_user = models.User(username=username)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists!')

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.UserOut]:
    users = db.query(models.User).offset(skip).limit(limit).all()
    return [u for u in users]

def get_user(id: int, db: Session):
    return schemas.UserOut.model_validate(db.query(models.User).filter(models.User.id == id).first())

def update_user(id: int, request: schemas.UserCreate, db: Session):
    user_obj = db.query(models.User).filter(models.User.id == id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist!')
    if request.username:
        user_obj.username = request.username.strip().lower()
    try:
        db.add(user_obj)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with given username already exists!"
        )
    return user_obj

def delete_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id: {id} not found.'
        )
    try:
        db.delete(user)
        db.commit()
    except IntegrityError: # could happen if there is no ondelete cascade in association table
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this user due to related constraints."
        )
