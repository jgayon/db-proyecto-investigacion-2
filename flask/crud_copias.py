from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

copias_bp = Blueprint('copias', __name__, url_prefix='/copias')

@copias_bp.route('/')
def listar_copias():
    copias = list(db.copias.find())
    ediciones = {
        ed['_id']: {
            'isbn': ed['isbn'],
            'libro': db.libros.find_one({'_id': ed['libro_id']})['titulo']
        } for ed in db.ediciones.find()
    }
    return render_template('copias/listar.html', copias=copias, ediciones=ediciones)

@copias_bp.route('/crear', methods=['GET', 'POST'])
def crear_copia():
    ediciones = list(db.ediciones.find())
    libros = {libro['_id']: libro['titulo'] for libro in db.libros.find()}
    if request.method == 'POST':
        edicion_id = request.form['edicion_id']
        numero = request.form['numero']
        db.copias.insert_one({
            'edicion_id': ObjectId(edicion_id),
            'numero': numero
        })
        return redirect(url_for('copias.listar_copias'))
    return render_template('copias/crear.html', ediciones=ediciones, libros=libros)

@copias_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_copia(id):
    copia = db.copias.find_one({'_id': ObjectId(id)})
    ediciones = list(db.ediciones.find())
    libros = {libro['_id']: libro['titulo'] for libro in db.libros.find()}
    if request.method == 'POST':
        edicion_id = request.form['edicion_id']
        numero = request.form['numero']
        db.copias.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'edicion_id': ObjectId(edicion_id),
                'numero': numero
            }
        })
        return redirect(url_for('copias.listar_copias'))
    return render_template('copias/editar.html', copia=copia, ediciones=ediciones, libros=libros)

@copias_bp.route('/eliminar/<id>')
def eliminar_copia(id):
    db.copias.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('copias.listar_copias'))
