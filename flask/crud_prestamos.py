from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId

prestamos_bp = Blueprint('prestamos', __name__, url_prefix='/prestamos')

# Ruta para listar todos los préstamos
@prestamos_bp.route('/')
def listar_prestamos():
    prestamos = list(db.prestamos.find())
    for prestamo in prestamos:
        prestamo['usuario'] = db.usuarios.find_one({'_id': prestamo['usuario_id']})
        prestamo['copia'] = db.copias.find_one({'_id': prestamo['copia_id']})
        prestamo['edicion'] = db.ediciones.find_one({'_id': prestamo['copia']['edicion_id']})
        prestamo['libro'] = db.libros.find_one({'_id': prestamo['edicion']['libro_id']})
    return render_template('prestamos/listar.html', prestamos=prestamos)

# Ruta para crear un nuevo préstamo
@prestamos_bp.route('/crear', methods=['GET', 'POST'])
def crear_prestamo():
    # Obtener lista de usuarios y copias disponibles de la base de datos
    usuarios = list(db.usuarios.find())
    copias_todas = list(db.copias.find())
    copias_prestadas_ids = [p['copia_id'] for p in db.prestamos.find()]
    copias_disponibles = [c for c in copias_todas if c['_id'] not in copias_prestadas_ids]

    # Si se ha enviado el formulario
    if request.method == 'POST':
        usuario_id = ObjectId(request.form['usuario_id'])
        copia_id = ObjectId(request.form['copia_id'])
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']

        # Insertar nuevo préstamo en la base de datos
        db.prestamos.insert_one({
            'usuario_id': usuario_id,
            'copia_id': copia_id,
            'fecha_prestamo': fecha_prestamo,
            'fecha_devolucion': fecha_devolucion
        })
        return redirect(url_for('prestamos.listar_prestamos'))

    # Recoger ediciones y libros
    ediciones = {e['_id']: e for e in db.ediciones.find()}
    libros = {l['_id']: l for l in db.libros.find()}

    return render_template('prestamos/crear.html', usuarios=usuarios,
                           copias=copias_disponibles, ediciones=ediciones, libros=libros)

# Ruta para eliminar un préstamo
@prestamos_bp.route('/eliminar/<id>')
def eliminar_prestamo(id):
    db.prestamos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('prestamos.listar_prestamos'))

# Ruta para editar un préstamo
@prestamos_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    prestamo = db.prestamos.find_one({'_id': ObjectId(id)})
    if not prestamo:
        return redirect(url_for('prestamos.listar_prestamos'))

    if request.method == 'POST':
        usuario_id = ObjectId(request.form['usuario_id'])
        copia_id = ObjectId(request.form['copia_id'])
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']

        db.prestamos.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'usuario_id': usuario_id,
                'copia_id': copia_id,
                'fecha_prestamo': fecha_prestamo,
                'fecha_devolucion': fecha_devolucion
            }}
        )
        return redirect(url_for('prestamos.listar_prestamos'))

    usuarios = list(db.usuarios.find())
    copias = list(db.copias.find())

    ediciones = {e['_id']: e for e in db.ediciones.find()}
    libros = {l['_id']: l for l in db.libros.find()}

    return render_template('prestamos/editar.html', prestamo=prestamo, usuarios=usuarios,
                           copias=copias, ediciones=ediciones, libros=libros)
