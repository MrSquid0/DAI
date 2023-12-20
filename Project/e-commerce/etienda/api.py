# etienda/api.py
from ninja_extra import NinjaExtraAPI
from typing import List
from ninja import  Schema
from ninja.security import HttpBearer
from pydantic import ValidationError
from . import mongo_operations_api
import logging

logger = logging.getLogger(__name__)


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


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "dai":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())


@api.get("/products", tags=['DAI SHOP'], response={200: List[ProductSchema]}, auth=None)
def get_list_of_products(request, start: int = 0, end: int = 10):
    products = mongo_operations_api.list_products(start, end)
    return products


@api.get("/products/{product_id}", tags=['DAI SHOP'], response={200: ProductSchema, 404: ErrorSchema}, auth=None)
def get_product(request, product_id: str):
    try:
        product = mongo_operations_api.get_product(product_id)
        return 200, product
    except:
        logger.error("The product was not found throughout the API!")
        return 404, {"message": "Product not found"}


@api.post("/products", tags=['DAI SHOP'], response={201: ProductSchema, 400: ErrorSchema})
def add_product(request, payload: ProductSchemaIn):
    if not payload.title or not payload.title[0].isupper():
        error_message = "The first letter of the product name must be uppercase."
        logger.error(f"There was a problem trying to add the product throughout the API! {error_message}")
        return 400, {"message": error_message}

    try:
        created_product = mongo_operations_api.create_product(payload)
        logger.info("A product was added throughout the API!")
        return 201, created_product
    except ValidationError as e:
        logger.error("There was a problem trying to add the product throughout the API!")
        return 400, {"message": str(e)}


@api.put("/products/{product_id}", tags=['DAI SHOP'], response={201: ProductSchema, 400: ErrorSchema})
def modify_product(request, product_id: str, payload: ProductSchemaIn):
    if not payload.title or not payload.title[0].isupper():
        error_message = "The first letter of the product name must be uppercase."
        logger.error(f"There was a problem trying to add the product throughout the API! {error_message}")
        return 400, {"message": error_message}

    try:
        data_modified = mongo_operations_api.modify_product(product_id, payload)
        logger.info("A product was added throughout the API!")
        return 201, data_modified
    except ValidationError as e:
        logger.error("There was a problem trying to add the product throughout the API!")
        return 400, {"message": str(e)}


@api.delete("/products/{product_id}", tags=['DAI SHOP'], response={204: None, 404: ErrorSchema})
def delete_product(request, product_id: str):
    try:
        mongo_operations_api.delete_product(product_id)
        logger.info("A product was deleted throughout the API!")
        return 204, None
    except:
        logger.error("There was a problem trying to delete the product throughout the API!")
        return 404, {"message": "Product not found"}


@api.put('/products/{product_id}/{rating}', tags=['DAI SHOP'], response={202: ProductSchema, 400: ErrorSchema})
def add_rating(request, product_id: str, rating: float):
    try:
        result = mongo_operations_api.modify_rating(product_id, rating)
        return 202, result
    except Exception as e:
        logger.error("There was a problem trying to modify the rating of a product throughout the API!")
        return 404, {"message": str(e)}


@api.get("/searchproduct", tags=['DAI SHOP'], response={202: list[ProductSchema], 400: ErrorSchema}, auth=None)
def search_product(request, product_info: str):
    try:
        products = mongo_operations_api.coincidences_by_name_or_description(product_info)
        return 202, products
    except Exception as e:
        logger.error("There was a problem trying to search a product throughout the API!")
        return 404, {"message": str(e)}
