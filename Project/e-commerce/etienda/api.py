# etienda/api.py
from ninja_extra import NinjaExtraAPI, api_controller, http_get
from typing import List
from ninja import NinjaAPI, Schema
from . import Queries
from pydantic import ValidationError, validator
from . import mongo_operations_api
import logging

logger = logging.getLogger(__name__)
api = NinjaExtraAPI()


class Rate(Schema):
    rate: float
    count: int


class ProductSchema(Schema):  # sirve para validar y para documentación
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate


class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate


class ErrorSchema(Schema):
    message: str


@api.get("/products", tags=['DAI SHOP'], response={200: List[ProductSchema]})
def get_list_of_products(request, start: int = 0, end: int = 10):
    products = mongo_operations_api.list_products(start, end)
    return products


@api.get("/products/{id}", tags=['DAI SHOP'], response={200: ProductSchema, 404: ErrorSchema})
def get_product(request, id: str):
    try:
        product = mongo_operations_api.search_product(id)
        return 200, product
    except:
        logger.error("The product was not found throughout the API!")
        return 404, {"message": "Product not found"}


@api.post("/products", tags=['DAI SHOP'], response={201: ProductSchema, 400: ErrorSchema})
def add_product(request, payload: ProductSchemaIn):
    try:
        created_product = mongo_operations_api.create_product(payload)
        logger.info("A product was added throughout the API!")
        return 201, created_product
    except ValidationError as e:
        logger.error("There was a problem trying to add the product throughout the API!")
        return 400, {"message": str(e)}


@api.put("/products/{id}", tags=['DAI SHOP'], response={202: ProductSchema, 404: ErrorSchema})
def modify_product(request, id: str, payload: ProductSchemaIn):
    try:
        modified_data = mongo_operations_api.modify_product(id, payload)
        logger.info("Some product information was modified throughout the API!")
        return 202, modified_data
    except:
        logger.error("There was a problem trying to modify the product throughout the API!")
        return 404, {"message": "Product not found"}


@api.delete("/products/{id}", tags=['DAI SHOP'], response={204: None, 404: ErrorSchema})
def delete_product(request, id: str):
    try:
        mongo_operations_api.delete_product(id)
        logger.info("A product was deleted throughout the API!")
        return 204, None
    except:
        logger.error("There was a problem trying to delete the product throughout the API!")
        return 404, {"message": "Product not found"}
