from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas


def create(request: schemas.RecipeCreate, db: Session, current_user: models.User) -> models.Recipe:
    try:
        new_recipe = models.Recipe(title=request.title,
                                   description = request.description,
                                   cooking_time = request.cooking_time,
                                   owner_id = current_user.id)
        ingredients_obj: List[models.Ingredient] = []
        # attach existing ingredients by id
        if request.ingredient_ids:
            existing = db.query(models.Ingredient).filter(models.Ingredient.id.in_(request.ingredient_ids)).all()
            if len(existing) != len(set(request.ingredient_ids)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more ingredient ids not found")
            ingredients_obj.extend(existing)
        
        # create or reuse ingredients by name
        for ing in request.ingredients:
            clean_name = ing.name.strip().lower()
            found = db.query(models.Ingredient).filter(models.Ingredient.name == clean_name).first()
            if found:
                ingredients_obj.append(found)
            else:
                new_ing = models.Ingredient(name=clean_name)
                db.add(new_ing)
                db.flush()
                ingredients_obj.append(new_ing)
        # set relationship
        new_recipe.ingredients = ingredients_obj
        db.add(new_recipe)
        db.commit() # good practice is to have one commit
        db.refresh(new_recipe)
        return new_recipe
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback() # after commit rollback doesnt work
        raise

def get_all(db: Session) -> List[models.Recipe]:
    recipes = db.query(models.Recipe).all()
    return [recipe for recipe in recipes]

def get_recipe(id: int, db: Session):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Recipe with id: {id} not found! ')
    return recipe

def update_recipe(id: int, request: schemas.RecipeCreate, db: Session):
    recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id)
    recipe = recipe_query.first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Recipe with {id} id not found')
    # recipe_query.update(request.model_dump()) bypasses orm
    if request.title is not None:
        recipe.title = request.title.strip()

    if request.description is not None:
        recipe.description = request.description.strip()

    if request.cooking_time is not None:
        recipe.cooking_time = request.cooking_time
    # Process ingredients (if provided)
    ingredients_to_attach = []

    if request.ingredient_ids:
        existing = (
            db.query(models.Ingredient)
            .filter(models.Ingredient.id.in_(request.ingredient_ids))
            .all()
        )
        if len(existing) != len(set(request.ingredient_ids)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more ingredient IDs not found."
            )
        ingredients_to_attach.extend(existing)

    for ing in request.ingredients or []:
        found = (
            db.query(models.Ingredient)
            .filter(models.Ingredient.name == ing.name.lower().strip())
            .first()
        )
        if found:
            ingredients_to_attach.append(found)
        else:
            new_ing = models.Ingredient(name=ing.name.lower().strip())
            db.add(new_ing)
            db.flush()  # ensures new_ing.id exists
            ingredients_to_attach.append(new_ing)
    
    if request.ingredient_ids or request.ingredients:
        recipe.ingredients = ingredients_to_attach
    
    try:
        db.commit()
        db.refresh(recipe)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Integrity error (maybe title or ingredient name already exists)."
        )
    return recipe

def delete_recipe(id: int, db: Session):
    recipe_to_delete = db.query(models.Recipe).filter(models.Recipe.id == id).first()
    if not recipe_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe with {id} not found.')
    try:
        db.delete(recipe_to_delete)
        db.commit()
    except IntegrityError: # could happen if there is no ondelete cascade in association table
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this ingredient due to related constraints."
        )
    return {"detail": f"Recipe with id {id} deleted successfully."}
