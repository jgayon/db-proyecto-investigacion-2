from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/biblioteca"
mongo = PyMongo(app)

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# --- RUTAS PRINCIPALES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/autores")
def ver_autores():
    autores = list(mongo.db.autores.find())
    return render_template("autores.html", autores=autores)

@app.route("/libros")
def ver_libros():
    libros = list(mongo.db.libros.find())
    return render_template("libros.html", libros=libros)

@app.route("/usuarios")
def ver_usuarios():
    usuarios = list(mongo.db.usuarios.find())
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/prestamos")
def ver_prestamos():
    prestamos = list(mongo.db.prestamos.find())
    return render_template("prestamos.html", prestamos=prestamos)

# --- CRUD AUTOR ---
@app.route("/autor", methods=["POST"])
def crear_autor():
    nombre = request.form["nombre"]
    mongo.db.autores.insert_one({"nombre": nombre})
    return redirect(url_for("ver_autores"))

# --- CRUD LIBRO ---
@app.route("/libro", methods=["POST"])
def crear_libro():
    titulo = request.form["titulo"]
    autor_id = ObjectId(request.form["autor_id"])
    mongo.db.libros.insert_one({"titulo": titulo, "autor_id": autor_id})
    return redirect(url_for("ver_libros"))

# --- CRUD USUARIO ---
@app.route("/usuario", methods=["POST"])
def crear_usuario():
    nombre = request.form["nombre"]
    rut = request.form["rut"]
    mongo.db.usuarios.insert_one({"nombre": nombre, "RUT": rut})
    return redirect(url_for("ver_usuarios"))

# --- CRUD PRESTAMO ---
@app.route("/prestamo", methods=["POST"])
def crear_prestamo():
    usuario_id = ObjectId(request.form["usuario_id"])
    copia_id = ObjectId(request.form["copia_id"])
    fecha = datetime.now()
    mongo.db.prestamos.insert_one({
        "usuario_id": usuario_id,
        "copia_id": copia_id,
        "fecha_prestamo": fecha
    })
    return redirect(url_for("ver_prestamos"))

if __name__ == "__main__":
    app.run(debug=True)