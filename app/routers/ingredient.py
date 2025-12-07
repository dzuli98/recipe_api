from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
from .. repository import ingredient
from typing import List

router = APIRouter(
    prefix='/ingredients',
    tags=['Ingredients']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.IngredientOut)
def create(request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    return ingredient.create(request, db)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.IngredientOut])
def all(db: Session = Depends(database.get_db)):
    return ingredient.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.IngredientOut)
def get_ingredient(id: int, db: Session = Depends(database.get_db)):
    return ingredient.get_ingredient(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.IngredientOut)
def update_ingredient(id: int, request: schemas.IngredientBase, db: Session = Depends(database.get_db)):
    return ingredient.update_ingredient(id, request, db)