from pymongo import MongoClient
import os

MONGO_DB_URL = "mongodb://mongo:mFQtqDptPLwZXKwVmnzihaywXxeORPfa@autorack.proxy.rlwy.net:59644"

# Crea la conexión a MongoDB
client = MongoClient(MONGO_DB_URL)
db = client.SentirseBienDB