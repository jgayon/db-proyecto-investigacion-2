from db import db

prestamos_collection = db["prestamos"]

result = prestamos_collection.delete_many({})
print(f"Préstamos eliminados: {result.deleted_count}")