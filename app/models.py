from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cooking_time = Column(Integer, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ingredients = relationship('Ingredient', back_populates='recipe', cascade='all, delete-orphan')

# one to many : recipe -> ingredient
# Foreign key goes on the "many" side.
class Ingredient(Base):
    __tablename__= 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship('Recipe', back_populates='ingredients')