from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate


def list_ingredients(db: Session):
    return db.query(Ingredient).order_by(Ingredient.id.desc()).all()


def get_ingredient(db: Session, ingredient_id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return ingredient


def create_ingredient(db: Session, payload: IngredientCreate):
    existing = db.query(Ingredient).filter(Ingredient.name == payload.name).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists",
        )

    ingredient = Ingredient(
        name=payload.name,
        unit=payload.unit,
        cost_per_unit=payload.cost_per_unit,
    )

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


def update_ingredient(db: Session, ingredient_id: int, payload: IngredientUpdate):
    ingredient = get_ingredient(db, ingredient_id)

    if payload.name is not None:
        duplicate = (
            db.query(Ingredient)
            .filter(Ingredient.name == payload.name, Ingredient.id != ingredient_id)
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another ingredient with this name already exists",
            )

        ingredient.name = payload.name

    if payload.unit is not None:
        ingredient.unit = payload.unit

    if payload.cost_per_unit is not None:
        ingredient.cost_per_unit = payload.cost_per_unit

    db.commit()
    db.refresh(ingredient)

    return ingredient


def delete_ingredient(db: Session, ingredient_id: int):
    ingredient = get_ingredient(db, ingredient_id)

    db.delete(ingredient)
    db.commit()

    return None