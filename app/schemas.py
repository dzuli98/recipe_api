from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str
    description: str
    cooking_time: int

class CreateRecipe(BaseRecipe):
    pass

class OutRecipe(BaseRecipe):
    id: int
    
    class Config:
        orm_mode = True