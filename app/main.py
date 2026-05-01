from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.models.ingredient import Ingredient
from app.routers.health import router as health_router
from app.routers.ingredient import router as ingredient_router

app = FastAPI(
    title="Sisasmik Kitchen API",
)

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(ingredient_router)


@app.get("/")
def root():
    return {"message": "API running"}