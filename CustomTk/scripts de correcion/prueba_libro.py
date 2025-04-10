# from pymongo import MongoClient
# from bson import ObjectId

# client = MongoClient("mongodb://localhost:27017")  # Ajusta si usas otra URL
# db = client["biblioteca"]  # Reemplaza por tu nombre real

# libros = db["libros"]

# for libro in libros.find():
#     print("Título:", libro.get("titulo"))
#     print("Autores (raw):", libro.get("autores"))
#     print("-" * 40)

    
from db import db

# Encuentra todos los libros que tienen el campo viejo 'autor_ids'
libros_con_autor_ids = db.libros.find({"autor_ids": {"$exists": True}})

for libro in libros_con_autor_ids:
    print(f"Actualizando libro: {libro.get('titulo', 'Sin título')}")
    db.libros.update_one(
        {"_id": libro["_id"]},
        {
            "$set": {"autores": libro["autor_ids"]},
            "$unset": {"autor_ids": ""}
        }
    )

print("Migración completada.")