from flask import Blueprint, render_template, request
from db import db
from bson.objectid import ObjectId

consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')

@consultas_bp.route('/')
def menu_consultas():
    return render_template('consultas/menu.html')


@consultas_bp.route('/consulta1')
def consulta1():
    copias = list(db.copias.find())
    ediciones = {str(e['_id']): e for e in db.ediciones.find()}
    libros = {str(l['_id']): l for l in db.libros.find()}
    autores = {str(a['_id']): a for a in db.autores.find()}

    data = []
    for copia in copias:
        edicion = ediciones.get(str(copia['edicion_id']))
        if not edicion:
            continue
        libro = libros.get(str(edicion['libro_id']))
        if not libro:
            continue
        libro_autores = [autores.get(str(aid))['nombre'] for aid in libro['autor_ids'] if str(aid) in autores]
        data.append({
            'copia_numero': copia['numero'],
            'isbn': edicion['isbn'],
            'anio': edicion['anio'],
            'idioma': edicion['idioma'],
            'titulo': libro['titulo'],
            'autores': libro_autores
        })

    return render_template('consultas/consulta1.html', datos=data)


@consultas_bp.route('/consulta2', methods=['GET', 'POST'])
def consulta2():
    datos = []
    if request.method == 'POST':
        rut = request.form['rut']
        usuario = db.usuarios.find_one({'rut': rut})
        if usuario:
            prestamos = list(db.prestamos.find({'usuario_id': usuario['_id']}))
            copias = {str(c['_id']): c for c in db.copias.find()}
            ediciones = {str(e['_id']): e for e in db.ediciones.find()}
            libros = {str(l['_id']): l for l in db.libros.find()}

            for prestamo in prestamos:
                copia = copias.get(str(prestamo['copia_id']))
                edicion = ediciones.get(str(copia['edicion_id'])) if copia else None
                libro = libros.get(str(edicion['libro_id'])) if edicion else None
                if copia and edicion and libro:
                    datos.append({
                        'titulo': libro['titulo'],
                        'isbn': edicion['isbn'],
                        'fecha_prestamo': prestamo['fecha_prestamo'],
                        'fecha_devolucion': prestamo['fecha_devolucion']
                    })
    return render_template('consultas/consulta2.html', datos=datos)
