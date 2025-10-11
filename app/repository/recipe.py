from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models

def create(request: schemas.CreateRecipe, db: Session) -> models.Recipe:
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
