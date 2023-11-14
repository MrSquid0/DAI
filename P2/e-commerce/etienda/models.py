from django.db import models

from pydantic import BaseModel, Field, EmailStr, field_serializer
from pathlib import Path
import pathlib
from pymongo import MongoClient
from datetime import datetime
from typing import Any
import requests
import Queries
import os

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
    rating: Nota

    @field_serializer('imágen')
    def serializaPath(self, val) -> str:
        if type(val) is pathlib.PosixPath:
            return str(val)
        return val


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list