#Eliminar Base de datos en Caso de emergencia

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
client.drop_database("biblioteca")
print("Base de datos 'biblioteca' eliminada por completo.")

client.close()