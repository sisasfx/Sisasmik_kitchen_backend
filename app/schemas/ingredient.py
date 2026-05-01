from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    unit: str = Field(..., min_length=1, max_length=20)
    cost_per_unit: float | None = Field(default=None, ge=0)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    unit: str | None = Field(default=None, min_length=1, max_length=20)
    cost_per_unit: float | None = Field(default=None, ge=0)


class IngredientRead(IngredientBase):
    id: int

    model_config = {"from_attributes": True}