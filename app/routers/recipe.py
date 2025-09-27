from fastapi import APIRouter, Depends
from ..repository import recipe
from .. import database, schemas

router = APIRouter()

@router.post('/recipe')
def create(request: schemas.CreateRecipe, db = Depends(database.get_db)):
    return recipe.create(request, db)