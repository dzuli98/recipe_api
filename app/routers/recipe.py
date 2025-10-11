from typing import List
from fastapi import APIRouter, Depends, status
from ..repository import recipe
from .. import database, schemas, models

router = APIRouter(
    prefix='/recipe',
    tags=['Recipes']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.OutRecipe)
def create(request: schemas.CreateRecipe, db = Depends(database.get_db)):
    return recipe.create(request, db)

@router.get('/', status_code=status.HTTP_404_NOT_FOUND ,response_model=List[schemas.OutRecipe])
def all(db = Depends(database.get_db)):
    return recipe.get_all(db)
