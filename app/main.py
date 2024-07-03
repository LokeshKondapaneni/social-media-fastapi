from fastapi import FastAPI
from .database import engine
from . import models
from .router import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    """
    The main landing page
    """
    return {"message": "Welcome to landing page of Posts"}