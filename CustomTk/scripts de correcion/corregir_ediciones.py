from pymongo import MongoClient
from bson import ObjectId

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017")
db = client["biblioteca"]  # Cambia por el nombre correcto de tu base de datos

ediciones = db["ediciones"]
libros = db["libros"]

# # Buscar ediciones sin 'libro_id'
# ediciones_invalidas = list(ediciones.find({"libro_id": {"$exists": False}}))

# print(f"Se encontraron {len(ediciones_invalidas)} ediciones sin 'libro_id'.\n")

# if not ediciones_invalidas:
#     exit()

# # Mostrar las ediciones afectadas
# for i, ed in enumerate(ediciones_invalidas):
#     print(f"{i+1}. ID: {ed['_id']}, ISBN: {ed.get('ISBN', 'Desconocido')}, Idioma: {ed.get('idioma', 'Desconocido')}")

# opcion = input("\n¿Qué deseas hacer con estas ediciones?\n1 - Asignar libro manualmente\n2 - Eliminar todas\nOpción: ")

# if opcion == "1":
#     # Listar libros existentes
#     libros_existentes = list(libros.find())
#     print("\nLibros disponibles:")
#     for i, libro in enumerate(libros_existentes):
#         print(f"{i+1}. {libro['titulo']} ({libro['_id']})")

#     for ed in ediciones_invalidas:
#         print(f"\nEditando edición ID: {ed['_id']}")
#         libro_idx = input("Selecciona el número del libro para asociar esta edición (o Enter para omitir): ")
#         if libro_idx.isdigit():
#             libro_idx = int(libro_idx) - 1
#             if 0 <= libro_idx < len(libros_existentes):
#                 libro_id = libros_existentes[libro_idx]['_id']
#                 ediciones.update_one(
#                     {"_id": ed["_id"]},
#                     {"$set": {"libro_id": ObjectId(libro_id)}}
#                 )
#                 print("✔ Libro asignado.")
#             else:
#                 print("❌ Índice inválido, edición omitida.")
#         else:
#             print("⏩ Edición omitida.")
# elif opcion == "2":
#     resultado = ediciones.delete_many({"libro_id": {"$exists": False}})
#     print(f"\n✅ Se eliminaron {resultado.deleted_count} ediciones.")
# else:
#     print("❌ Opción inválida. No se hicieron cambios.")


# archivo: fix_ediciones_libro_id.py

from pymongo import MongoClient
from bson import ObjectId

ediciones_collection = db["ediciones"]

# Recorrer ediciones y corregir libro_id si está como string
ediciones_corregidas = 0

for ed in ediciones_collection.find():
    libro_id = ed.get("libro_id")
    if isinstance(libro_id, str):
        try:
            nuevo_id = ObjectId(libro_id)
            ediciones_collection.update_one(
                {"_id": ed["_id"]},
                {"$set": {"libro_id": nuevo_id}}
            )
            ediciones_corregidas += 1
        except Exception as e:
            print(f"Error al convertir ID en edición {ed['_id']}: {e}")

print(f"✅ Ediciones corregidas: {ediciones_corregidas}")
