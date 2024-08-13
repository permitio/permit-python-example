

from fastapi import FastAPI
from app.database import models
from app.database.database import engine
from app.routers import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "hello design_app_db!"}

