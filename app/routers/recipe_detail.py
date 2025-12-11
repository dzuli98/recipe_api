from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import database, schemas
from ..repository import recipe_detail as recipe_detail_repo

router = APIRouter(prefix="/recipe-details", tags=["Recipe Details"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipeDetailOut)
def create(request: schemas.RecipeDetailCreate, db: Session = Depends(database.get_db)):
    recipe_detail = recipe_detail_repo.create(request, db)
    return schemas.RecipeDetailOut.model_validate(recipe_detail)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.RecipeDetailOut])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    recipe_details = recipe_detail_repo.get_all(db, skip=skip, limit=limit)
    return [schemas.RecipeDetailOut.model_validate(rd) for rd in recipe_details]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.RecipeDetailOut)
def get_recipe_detail(id: int, db: Session = Depends(database.get_db)):
    recipe_detail = recipe_detail_repo.get_recipe_detail(id, db)
    return schemas.RecipeDetailOut.model_validate(recipe_detail)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.RecipeDetailOut)
def update(id: int, request: schemas.RecipeDetailCreate, db: Session = Depends(database.get_db)):
    recipe_detail = recipe_detail_repo.update_recipe_detail(id, request, db)
    return schemas.RecipeDetailOut.model_validate(recipe_detail)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    recipe_detail_repo.delete_recipe_detail(id, db)
    return None