from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

libros_bp = Blueprint('libros', __name__, url_prefix='/libros')

@libros_bp.route('/')
def listar_libros():
    libros = list(db.libros.find())
    autores = {str(a['_id']): a['nombre'] for a in db.autores.find()}
    return render_template('libros/listar.html', libros=libros, autores=autores)

@libros_bp.route('/crear', methods=['GET', 'POST'])
def crear_libro():
    autores = list(db.autores.find())
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        db.libros.insert_one({
            'titulo': titulo,
            'autor_ids': [ObjectId(autor_id)]
        })
        return redirect(url_for('libros.listar_libros'))
    return render_template('libros/crear.html', autores=autores)

@libros_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_libro(id):
    libro = db.libros.find_one({'_id': ObjectId(id)})
    autores = list(db.autores.find())
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        db.libros.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'titulo': titulo, 'autor_ids': [ObjectId(autor_id)]}}
        )
        return redirect(url_for('libros.listar_libros'))
    return render_template('libros/editar.html', libro=libro, autores=autores)

@libros_bp.route('/eliminar/<id>')
def eliminar_libro(id):
    db.libros.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('libros.listar_libros'))
