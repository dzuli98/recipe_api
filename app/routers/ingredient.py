from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import ingredient as ingredient_repo

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.IngredientOut)
def create(request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    ingredient = ingredient_repo.create(request, db)
    return schemas.IngredientOut.model_validate(ingredient)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.IngredientOut])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    ingredients = ingredient_repo.get_all(db, skip=skip, limit=limit)
    return [schemas.IngredientOut.model_validate(ing) for ing in ingredients]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.IngredientOut)
def get_ingredient(id: int, db: Session = Depends(database.get_db)):
    ingredient = ingredient_repo.get_ingredient(id, db)
    return schemas.IngredientOut.model_validate(ingredient)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.IngredientOut)
def update(id: int, request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    ingredient = ingredient_repo.update_ingredient(id, request, db)
    return schemas.IngredientOut.model_validate(ingredient)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    ingredient_repo.delete_ingredient(id, db)
    return None