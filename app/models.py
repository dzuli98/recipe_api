from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many realationship
# in ingredient we would need to add a list of recipe ids to which it belongs -> NOT POSSIBLE
# So the database needs a middle table to store pairs: recipe_id -> ingredient_id
# Hey SQLAlchemy, to see which ingredients belong to a recipe, go through the recipe_ingredient table.
# added on delete only here
# dont add ondelete in models then, because if i would add cascade='all, delete-orphan' in ingredient for example
# If I remove an Ingredient from Recipe.ingredients, also DELETE that Ingredient from the database

recipe_ingredient = Table(
    'recipe_ingredient',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True), # ondelete -> if recipe 1 is deleted remove all the rows together with ingr_id
    Column('ingredient_id', Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True)
)

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cooking_time = Column(Integer, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ingredients = relationship('Ingredient', secondary=recipe_ingredient, back_populates='recipes')
    # one to many
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="recipes")
    # one to one
    details = relationship("RecipeDetails", back_populates="recipe", uselist=False)

class Ingredient(Base):
    __tablename__= 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship('Recipe', secondary=recipe_ingredient, back_populates='ingredients')

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="owner", cascade="all, delete-orphan") # cascade goes to parent relationship, parent controls deletions behaviour

class RecipeDetails(Base):
    __tablename__ = 'recipe_details'
    id = Column(Integer, primary_key=True, index=True)
    calories = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), unique=True)
    recipe = relationship("Recipe", back_populates="details")
