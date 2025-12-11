from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas


def create(request: schemas.IngredientCreate, db: Session):
    try:
        clean_name = request.name.strip().lower()
        existing = db.query(models.Ingredient).filter(models.Ingredient.name == clean_name).first()
        if existing:
            return existing
        new_ing = models.Ingredient(name=clean_name)
        db.add(new_ing)
        db.commit()
        db.refresh(new_ing)
        return new_ing
    except IntegrityError: # it may happen if another user meanwhile inserted the same ingredient
        db.rollback() 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already exists")

def get_all(db: Session ) -> List[schemas.IngredientOut]:
    return [ing for ing in db.query(models.Ingredient).all()]

def get_ingredient(id: int, db: Session):
    return db.query(models.Ingredient).filter(models.Ingredient.id == id).first()

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
    return ing_obj

# query.delete() → direct SQL, fast, no ORM cascade/events
# db.delete(obj) → ORM-managed, slower, triggers cascade and events
def delete_ingredient(id: int, db: Session):
    ing= db.query(models.Ingredient).filter(models.Ingredient.id == id).first()
    if not ing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ingredient with id: {id} not found.'
        )
    try:
        db.delete(ing)
        db.commit()
    except IntegrityError: # could happen if there is no ondelete cascade in association table
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this ingredient due to related constraints."
        )
