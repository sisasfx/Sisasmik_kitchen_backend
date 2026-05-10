from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.ingredient import IngredientCreate, IngredientRead, IngredientUpdate
import app.services.ingredient_services as ingredient_service

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return ingredient_service.list_ingredients(db)


@router.get("/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    return ingredient_service.get_ingredient(db, ingredient_id)


@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
def create_ingredient(payload: IngredientCreate, db: Session = Depends(get_db)):
    return ingredient_service.create_ingredient(db, payload)


@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_id: int,
    payload: IngredientUpdate,
    db: Session = Depends(get_db),
):
    return ingredient_service.update_ingredient(db, ingredient_id, payload)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    return ingredient_service.delete_ingredient(db, ingredient_id)