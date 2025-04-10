from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

ediciones_bp = Blueprint('ediciones', __name__, url_prefix='/ediciones')

@ediciones_bp.route('/')
def listar_ediciones():
    ediciones = list(db.ediciones.find())
    libros = {libro['_id']: libro['titulo'] for libro in db.libros.find()}
    return render_template('ediciones/listar.html', ediciones=ediciones, libros=libros)

@ediciones_bp.route('/crear', methods=['GET', 'POST'])
def crear_edicion():
    libros = list(db.libros.find())
    if request.method == 'POST':
        libro_id = request.form['libro_id']
        isbn = request.form['isbn']
        anio = request.form['anio']
        idioma = request.form['idioma']
        db.ediciones.insert_one({
            'libro_id': ObjectId(libro_id),
            'isbn': isbn,
            'anio': anio,
            'idioma': idioma
        })
        return redirect(url_for('ediciones.listar_ediciones'))
    return render_template('ediciones/crear.html', libros=libros)

@ediciones_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_edicion(id):
    edicion = db.ediciones.find_one({'_id': ObjectId(id)})
    libros = list(db.libros.find())
    if request.method == 'POST':
        libro_id = request.form['libro_id']
        isbn = request.form['isbn']
        anio = request.form['anio']
        idioma = request.form['idioma']
        db.ediciones.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'libro_id': ObjectId(libro_id),
                'isbn': isbn,
                'anio': anio,
                'idioma': idioma
            }
        })
        return redirect(url_for('ediciones.listar_ediciones'))
    return render_template('ediciones/editar.html', edicion=edicion, libros=libros)

@ediciones_bp.route('/eliminar/<id>')
def eliminar_edicion(id):
    db.ediciones.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('ediciones.listar_ediciones'))
