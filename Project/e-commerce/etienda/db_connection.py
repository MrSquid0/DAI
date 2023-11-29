from pymongo import MongoClient

def get_client():
    return MongoClient('mongo', 27017)