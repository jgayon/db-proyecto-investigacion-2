from db import db
from bson import ObjectId
from bson.errors import InvalidId

prestamos_collection = db["prestamos"]

# Eliminar préstamos con usuario_id inválido
for prestamo in prestamos_collection.find():
    try:
        ObjectId(prestamo["usuario_id"])
    except (InvalidId, TypeError):
        print("Eliminando:", prestamo)
        prestamos_collection.delete_one({"_id": prestamo["_id"]})