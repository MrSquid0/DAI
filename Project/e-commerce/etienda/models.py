import os

from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError, validator
from datetime import datetime
from typing import Any
from . import Queries


class Nota(BaseModel):
    puntuación: float = Field(ge=0., lt=5.)
    cuenta: int = Field(ge=1)


class Producto(BaseModel):
    _id: Any
    producto_id: int
    nombre: str
    precio: float
    descripción: str
    categoría: str
    imágen: str | None
    rating: Nota | None

    @validator('nombre')
    def validate_title(cls, value):
        if not value or not value[0].isupper():
            raise ValueError("The first letter of the title must be uppercase.")
        return value

    @validator('precio')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("The price cannot be below 0.")
        return value

    @validator('descripción')
    def validate_description(cls, value):
        if len(value) < 100:
            raise ValueError("The description must have at least 100 characters.")
        return value

    @validator('categoría')
    def validate_category(cls, value):
        categories = Queries.categories()
        if value not in categories:
            raise ValueError("The category is not valid.")
        return value


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list
