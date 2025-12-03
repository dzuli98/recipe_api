from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models

def create(request: schemas.Recipe, db: Session) -> models.Recipe:
    new_recipe = models.Recipe(title=request.title,
                               description = request.description,
                               cooking_time = request.cooking_time)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_all(db: Session) -> List[models.Recipe]:
    recipes = db.query(models.Recipe).all()
    return recipes

def update_recipe(id: int, request: schemas.Recipe, db: Session):
    recipe_query = db.query(models.Recipe).filter(models.Recipe.id == id)
    recipe_obj = recipe_query.first()
    if not recipe_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe with {id} id not found')
    recipe_query.update(request.model_dump())
    db.commit()
    db.refresh(recipe_obj) # updating the memory object
    # without this recipe_obj would not contain the updated values
    # in /docs the correct data will be returned
    # When Pydantic tries to access the attributes of recipe_obj (like title, description, etc.), SQLAlchemy detects that 
    # these attributes are expired.
    # SQLAlchemy then automatically reloads the data for those attributes from the database,
    return recipe_obj

def delete_recipe(id: int, db: Session):
    recipe_to_delete = db.query(models.Recipe).filter(models.Recipe.id == id)
    if not recipe_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe with {id} not found.')
    recipe_to_delete.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"Recipe with id {id} deleted successfully."}
