from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

autores_bp = Blueprint('autores', __name__, url_prefix='/autores')

@autores_bp.route('/')
def listar_autores():
    autores = list(db.autores.find())
    return render_template('autores/listar.html', autores=autores)

@autores_bp.route('/crear', methods=['GET', 'POST'])
def crear_autor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        db.autores.insert_one({'nombre': nombre})
        return redirect(url_for('autores.listar_autores'))
    return render_template('autores/crear.html')

@autores_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_autor(id):
    autor = db.autores.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nombre = request.form['nombre']
        db.autores.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre}})
        return redirect(url_for('autores.listar_autores'))
    return render_template('autores/editar.html', autor=autor)

@autores_bp.route('/eliminar/<id>')
def eliminar_autor(id):
    db.autores.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('autores.listar_autores'))