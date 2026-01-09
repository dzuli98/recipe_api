from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    detail: str

class BaseRecipe(BaseModel):
    title: str = Field(..., example="Delicious Pizza")  # Use example for better documentation
    description: str = Field(..., example="A cheesy pizza with fresh ingredients")
    cooking_time: int = Field(..., example=30)  # Example cooking time in minutes

class IngredientBase(BaseModel):
    name: str = Field(..., example="Tomato")  # Example ingredient name

class IngredientCreate(IngredientBase):
    pass  # No changes needed here

class IngredientOut(IngredientBase):
    id: int
    model_config = {'from_attributes': True}  # Tells Pydantic how to read data

class IngredientUpdate(IngredientBase):
    pass
# with mutable obj like list, if i would define it here, all instances would share the same list
class RecipeCreate(BaseRecipe):
    ingredient_ids: List[int] = Field(default_factory=list, example=[1, 2])  # Example IDs
    ingredients: List[IngredientCreate] = Field(default_factory=list, example=[{"name": "Cheese"}, {"name": "Tomato"}])  # Example nested ingredients

class RecipeOut(BaseRecipe):
    id: int
    ingredients: List[IngredientOut] = Field(default_factory=list)
    model_config = {
        "from_attributes": True
    }

class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated Pizza Title")
    description: Optional[str] = Field(None, example="Updated description of the pizza")
    cooking_time: Optional[int] = Field(None, example=25)  # Example updated cooking time
    ingredient_ids: Optional[List[int]] = Field(None, example=[1, 2])  # Example ingredient IDs
    ingredients: Optional[List[IngredientCreate]] = Field(None, example=[{"name": "Olive Oil"}])  # Example nested ingredients

class BaseUser(BaseModel):
    username: str = Field(..., example="username")

class UserCreate(BaseUser):
    password : str = Field(...,min_length=6, example='strongpassword')

class UserOut(BaseUser):
    id: int
    model_config = {
        "from_attributes": True
    }  

class UserUpdate(BaseUser):
    username: Optional[str] = Field(None, example="username")

class BaseRecipeDetail(BaseModel):
    calories: int = Field(..., ge=0)

class RecipeDetailCreate(BaseRecipeDetail):
    recipe_id: int

class RecipeDetailOut(BaseRecipeDetail):
    id: int
    model_config = {
        "from_attributes": True
    }

class RecipeDetailUpdate(BaseRecipeDetail):
    pass

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class NutritionItem(BaseModel):
    ingredient: str
    nutrients: dict | None = None
    error: str | None = None

class NutritionResponse(BaseModel):
    recipe_id: int
    nutrition: List[NutritionItem]

class EmailRequest(BaseModel):
    recipient: str = Field(...)
    subject: str = Field(...)
    body: str = Field(...)