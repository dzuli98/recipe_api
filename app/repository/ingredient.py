from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, database, models
from typing import List


def create(request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    try:
        clean_name = request.name.strip().lower()
        existing = db.query(models.Ingredient).filter(models.Ingredient.name == clean_name).first()
        if existing:
            return schemas.IngredientOut.model_validate(existing)
        new_ing = models.Ingredient(name=clean_name)
        db.add(new_ing)
        db.commit()
        db.refresh(new_ing)
        return schemas.IngredientOut.model_validate(new_ing)
    except IntegrityError: # it may happen if another user meanwhile inserted the same ingredient
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already exists")

def get_all(db: Session ) -> List[schemas.IngredientOut]:
    return [schemas.IngredientOut.model_validate(ing) for ing in db.query(models.Ingredient).all()]

def get_ingredient(id: int, db: Session):
    return schemas.IngredientOut.model_validate(db.query(models.Ingredient).filter(models.Ingredient.id == id).first())

def update_ingredient(id: int, request: schemas.IngredientCreate, db: Session):
    ing_query = db.query(models.Ingredient).filter(models.Ingredient.id == id)
    ing_obj = ing_query.first()
    if not ing_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ingredient with id: {id} not found.'
        )
    ing_obj.name = request.name.strip().lower()

    try:
        db.commit()
        db.refresh(ing_obj)
    except IntegrityError: # if you try to rename to to already existing ingredient
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ingredient with this name already exists."
        )
    return schemas.IngredientOut.model_validate(ing_obj)