# app.py
from flask import Flask, render_template
from db import db
from crud_autores import autores_bp
from crud_libros import libros_bp
from crud_ediciones import ediciones_bp
from crud_copias import copias_bp
from crud_usuarios import usuarios_bp
from crud_prestamos import prestamos_bp
from crud_consultas import consultas_bp

app = Flask(__name__)
app.register_blueprint(autores_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(ediciones_bp)
app.register_blueprint(copias_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(prestamos_bp)
app.register_blueprint(consultas_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
