from fastapi import FastAPI
from .database import engine
from . import models
from .routers import recipe

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def say_hello():
    return {"message": "This is working!"}

app.include_router(recipe.router)
models.Base.metadata.create_all(engine)
 