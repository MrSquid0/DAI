# etienda/api.py
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()


# function based definition
@api.get("/add", tags=['Aritmética'])
def add(request, a: int, b: int):
    return {"ok": "yes", "data": {"suma": a + b, "resta": a - b}}