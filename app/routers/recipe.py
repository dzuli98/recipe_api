from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..repository import recipe
from .. import database, schemas, models

router = APIRouter(
    prefix='/recipe',
    tags=['Recipes']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.RecipeOut)
def create(request: schemas.RecipeCreate, db: Session = Depends(database.get_db)):
    return recipe.create(request, db)

'''@router.get('/', status_code=status.HTTP_200_OK ,response_model=List[schemas.OutRecipe])
def all(db: Session = Depends(database.get_db)):
    return recipe.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OutRecipe)
def get_recipe(id, db: Session = Depends(database.get_db)):
    return recipe.get_recipe(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.OutRecipe)
def update_recipe(id, request: schemas.Recipe, db: Session = Depends(database.get_db)):
    return recipe.update_recipe(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(id, db: Session = Depends(database.get_db)):
    return recipe.delete_recipe(id, db)'''