from sqlalchemy.orm import Session
from .. import schemas

def create(request:schemas.CreateRecipe, db: Session):
    print('Test')