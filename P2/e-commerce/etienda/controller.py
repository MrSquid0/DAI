from . import Queries
from . import db_connection

def run_query_one():
    client = db_connection.get_client()
    return list(Queries.query1(client.tienda.productos))

def run_query_two():
    client = db_connection.get_client()
    return list(Queries.query2(client.tienda.productos))

def run_query_three():
    client = db_connection.get_client()
    return list(Queries.query3(client.tienda.productos))

def run_query_four():
    client = db_connection.get_client()
    return list(Queries.query4(client.tienda.productos))

def run_query_five():
    client = db_connection.get_client()
    return Queries.query5(client.tienda.productos, client.tienda.compras)

def run_query_six():
    client = db_connection.get_client()
    return Queries.query6(client.tienda.productos, client.tienda.compras)