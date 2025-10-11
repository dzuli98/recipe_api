from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str
    description: str
    cooking_time: int

class CreateRecipe(BaseRecipe):
    pass

class OutRecipe(BaseRecipe):
    id: int
    
    model_config = {
        "from_attributes": True
    }