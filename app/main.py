

from fastapi import FastAPI
from app.routers.auth import auth
from app.routers.comments import comments
from app.routers.designs import designs
from contextlib import asynccontextmanager
from app.database.database import sessionmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()



app = FastAPI(lifespan=lifespan)


app.include_router(auth.router)
app.include_router(designs.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "hello design_app_db!"}

