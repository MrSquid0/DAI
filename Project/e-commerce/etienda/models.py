import os

from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError, validator
from datetime import datetime
from typing import Any


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
    def validate_first_letter(cls, value):
        if not value or not value[0].isupper():
            raise ValueError("The first letter of the name of the product must be uppercase.")
        return value


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list
