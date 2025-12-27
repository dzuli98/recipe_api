from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from . import models, settings
from .routers import recipe, ingredient, user, recipe_detail, authentication

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Validate settings
    settings.settings
    yield
    # Shutdown: Add cleanup if needed

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def say_hello():
    return {"message": "This is working!"}

app.include_router(authentication.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)
app.include_router(user.router)
app.include_router(recipe_detail.router)
models.Base.metadata.create_all(engine)
 