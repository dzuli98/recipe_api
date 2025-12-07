from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    detail: str
    
class BaseRecipe(BaseModel):
    title: str
    description: str
    cooking_time: int

class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    # id will be automatically created by sqlalchemy
    pass

class IngredientOut(IngredientBase):
    id: int
    model_config = {'from_attributes': True} # if just tells pydantic how to read data

class RecipeCreate(BaseRecipe):
    ingredient_ids: List[int] = []
    ingredients: List[IngredientCreate] = []

class RecipeOut(BaseRecipe):
    id: int
    ingredients: List[IngredientOut] = []
    model_config = {
        "from_attributes": True
    }