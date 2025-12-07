from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
from .. repository import ingredient

router = APIRouter(
    prefix='/ingredient',
    tags=['Ingredients']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.IngredientOut)
def create(request: schemas.IngredientCreate, db: Session = Depends(database.get_db)):
    return ingredient.create(request, db)