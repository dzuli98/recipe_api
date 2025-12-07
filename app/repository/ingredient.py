from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, database, models


def create(request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    try:
        existing = db.query(models.Ingredient).filter(models.Ingredient.name == request.name).first()
        if existing:
            return schemas.IngredientOut.model_validate(existing)
        new_ing = models.Ingredient(name=request.name)
        db.add(new_ing)
        db.commit()
        db.refresh(new_ing)
        return schemas.IngredientOut.model_validate(new_ing)
    except IntegrityError: # it may happen if another user meanwhile inserted the same ingredient
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingredient already exists")