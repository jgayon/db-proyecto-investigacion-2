from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
def listar_usuarios():
    usuarios = list(db.usuarios.find())
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        db.usuarios.insert_one({'rut': rut, 'nombre': nombre})
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/crear.html')

@usuarios_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = db.usuarios.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        db.usuarios.update_one({'_id': ObjectId(id)}, {'$set': {'rut': rut, 'nombre': nombre}})
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/editar.html', usuario=usuario)

@usuarios_bp.route('/eliminar/<id>')
def eliminar_usuario(id):
    db.usuarios.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('usuarios.listar_usuarios'))
