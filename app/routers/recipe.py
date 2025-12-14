from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, database, oauth2, models
from ..repository import recipe as recipe_repo

router = APIRouter(prefix="/recipe", tags=["Recipes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipeOut)
def create(request: schemas.RecipeCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    recipe = recipe_repo.create(request, db, current_user)
    return schemas.RecipeOut.model_validate(recipe)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.RecipeOut])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    recipes = recipe_repo.get_all(db, skip=skip, limit=limit)
    return [schemas.RecipeOut.model_validate(recipe) for recipe in recipes]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.RecipeOut)
def get_recipe(id: int, db: Session = Depends(database.get_db)):
    recipe = recipe_repo.get_recipe(id, db)
    return schemas.RecipeOut.model_validate(recipe)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.RecipeOut)
def update(id: int, request: schemas.RecipeCreate, db: Session = Depends(database.get_db)):
    recipe = recipe_repo.update_recipe(id, request, db)
    return schemas.RecipeOut.model_validate(recipe)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    recipe_repo.delete_recipe(id, db)
    return None
