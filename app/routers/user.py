from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import user as user_repo

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = user_repo.create(request, db)
    return schemas.UserOut.model_validate(user)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def all(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = user_repo.get_all(db, skip=skip, limit=limit)
    return [schemas.UserOut.model_validate(u) for u in users]


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = user_repo.get_user(id, db)
    return schemas.UserOut.model_validate(user)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user(id: int, request: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    user = user_repo.update_user(id, request, db)
    return schemas.UserOut.model_validate(user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user_repo.delete_user(id, db)
    return None