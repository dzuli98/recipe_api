from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from . import models, settings
from .routers import recipe, ingredient, user, recipe_detail, authentication, cashing_router, ratelimit, background_tasks, tasks
from .core.redis_client import redis_client


async def lifespan(app: FastAPI):
    # Startup: validate Redis
    await redis_client.check_redis_connection()
    yield  # Hand over control to the app
    # Shutdown: cleanup if needed
    await redis_client.client.close()

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
app.include_router(cashing_router.router)
app.include_router(ratelimit.router)
app.include_router(background_tasks.router)
app.include_router(tasks.router)
models.Base.metadata.create_all(engine)
 