from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas


def create(request: schemas.RecipeDetailCreate, db: Session):
    try:
        # Check if this recipe already has details
        recipe_detail_obj = (
            db.query(models.RecipeDetails)
            .filter(models.RecipeDetails.recipe_id == request.recipe_id)
            .first()
        )

        if recipe_detail_obj:
            # Already exists → return existing details
            return recipe_detail_obj

        # Create new details
        recipe_detail_obj = models.RecipeDetails(
            calories=request.calories,
            recipe_id=request.recipe_id
        )

        db.add(recipe_detail_obj)
        db.commit()
        db.refresh(recipe_detail_obj)

        return recipe_detail_obj

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Details for this recipe already exist or recipe does not exist."
        )

def get_all(db: Session ) -> List[schemas.RecipeDetailOut]:
    return [recipe_detail for recipe_detail in db.query(models.RecipeDetails).all()]

def get_recipe_detail(id: int, db: Session):
    return db.query(models.RecipeDetails).filter(models.RecipeDetails.id == id).first()

def update_recipe_detail(id: int, request: schemas.RecipeDetailCreate, db: Session):
    recipe_detail_obj = db.query(models.RecipeDetails).filter(models.RecipeDetails.id == id).first()
    if not recipe_detail_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe detail with id: {id} does not exist!')
    if request.calories:
        recipe_detail_obj.calories = request.calories
    try:
        db.add(recipe_detail_obj)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe detail with given username already exists!"
        )
    return recipe_detail_obj

def delete_recipe_detail(id: int, db: Session):
    recipe_detail = db.query(models.RecipeDetails).filter(models.RecipeDetails.id == id).first()
    if not recipe_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Recipe Detail with id: {id} not found.'
        )
    try:
        db.delete(recipe_detail)
        db.commit()
    except IntegrityError: # could happen if there is no ondelete cascade in association table
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this recipe_detail due to related constraints."
        )
