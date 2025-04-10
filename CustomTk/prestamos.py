import customtkinter as ctk
import tkinter as tk
from bson import ObjectId
from db import db
from datetime import datetime

prestamos_collection = db["prestamos"]
usuarios_collection = db["usuarios"]
copias_collection = db["copias"]
ediciones_collection = db["ediciones"]
libros_collection = db["libros"]

def crear_tab_prestamos(frame):
    def cargar_usuarios():
        usuarios = usuarios_collection.find()
        valores = [f"{usuario['_id']} - {usuario['nombre']}" for usuario in usuarios]
        combobox_usuarios.configure(values=valores)
        if valores:
            combobox_usuarios.set(valores[0])

    def cargar_copias_disponibles():
        prestamos = prestamos_collection.find()
        copias_prestadas = {str(prestamo["copia_id"]) for prestamo in prestamos}
        
        opciones = []
        for copia in copias_collection.find():
            if str(copia["_id"]) in copias_prestadas:
                continue  # Saltar las copias ya prestadas

            edicion_id = copia.get("edicion_id")
            try:
                edicion = ediciones_collection.find_one({"_id": ObjectId(edicion_id)})
            except:
                edicion = None

            libro = None
            if edicion:
                try:
                    libro = libros_collection.find_one({"_id": ObjectId(edicion["libro_id"])})
                except:
                    libro = None

            titulo = libro["titulo"] if libro else "Libro desconocido"
            opciones.append(f"{copia['_id']} - Copia N°{copia['numero']} - {titulo}")
        
        combobox_copias.configure(values=opciones)
        if opciones:
            combobox_copias.set(opciones[0])

    def agregar_prestamo():
        usuario_texto = combobox_usuarios.get()
        copia_texto = combobox_copias.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion = entry_fecha_devolucion.get()

        if not usuario_texto or not copia_texto or not fecha_prestamo or not fecha_devolucion:
            return

        usuario_id = usuario_texto.split(" - ")[0]
        copia_id = copia_texto.split(" - ")[0]

        try:
            fecha_prestamo = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
            fecha_devolucion = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
        except ValueError:
            return  # Formato de fecha inválido

        prestamos_collection.insert_one({
            "usuario_id": ObjectId(usuario_id),
            "copia_id": ObjectId(copia_id),
            "fecha_prestamo": fecha_prestamo,
            "fecha_devolucion": fecha_devolucion
        })
        cargar_lista()
        cargar_copias_disponibles()

    def eliminar_prestamo():
        seleccion = listbox.curselection()
        if not seleccion:
             return
        texto = listbox.get(seleccion[0])
        prestamo_id = texto.split(" - ")[0]
        prestamos_collection.delete_one({"_id": ObjectId(prestamo_id)})
        cargar_lista()
        cargar_copias_disponibles()
    
    def actualizar_prestamo():
        seleccion = listbox.curselection()
        if not seleccion:
            return
        texto = listbox.get(seleccion[0])
        prestamo_id = texto.split(" - ")[0]

        usuario_texto = combobox_usuarios.get()
        copia_texto = combobox_copias.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion = entry_fecha_devolucion.get()

        if not usuario_texto or not copia_texto or not fecha_prestamo or not fecha_devolucion:
            return

        usuario_id = usuario_texto.split(" - ")[0]
        copia_id = copia_texto.split(" - ")[0]

        try:
            fecha_prestamo = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
            fecha_devolucion = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
        except ValueError:
            return

        prestamos_collection.update_one(
            {"_id": ObjectId(prestamo_id)},
            {"$set": {
                "usuario_id": ObjectId(usuario_id),
                "copia_id": ObjectId(copia_id),
                "fecha_prestamo": fecha_prestamo,
                "fecha_devolucion": fecha_devolucion
            }}
        )
        cargar_lista()
        cargar_copias_disponibles()

    def cargar_lista():
        listbox.delete(0, tk.END)
        for prestamo in prestamos_collection.find():
            try:
                usuario = usuarios_collection.find_one({"_id": ObjectId(prestamo["usuario_id"])})
                copia = copias_collection.find_one({"_id": ObjectId(prestamo["copia_id"])})

                edicion = ediciones_collection.find_one({"_id": ObjectId(copia["edicion_id"])}) if copia else None
                libro = libros_collection.find_one({"_id": ObjectId(edicion["libro_id"])}) if edicion else None

                nombre_usuario = usuario["nombre"] if usuario else "Usuario desconocido"
                numero_copia = copia["numero"] if copia else "?"
                titulo_libro = libro["titulo"] if libro else "Libro desconocido"

                f_prestamo = prestamo.get("fecha_prestamo", "").strftime("%Y-%m-%d") if "fecha_prestamo" in prestamo else "?"
                f_devolucion = prestamo.get("fecha_devolucion", "").strftime("%Y-%m-%d") if "fecha_devolucion" in prestamo else "?"

                texto = f"{prestamo['_id']} - {nombre_usuario} - Copia N°{numero_copia} - {titulo_libro} - Prestamo: {f_prestamo} - {f_devolucion}"
                listbox.insert(tk.END, texto)
            except:
                continue

    ctk.CTkLabel(frame, text="Usuario:").pack()
    combobox_usuarios = ctk.CTkComboBox(frame, values=[])
    combobox_usuarios.pack()

    ctk.CTkLabel(frame, text="Copia:").pack()
    combobox_copias = ctk.CTkComboBox(frame, values=[])
    combobox_copias.pack()

    ctk.CTkLabel(frame, text="Fecha Préstamo (YYYY-MM-DD):").pack()
    entry_fecha_prestamo = ctk.CTkEntry(frame)
    entry_fecha_prestamo.pack()

    ctk.CTkLabel(frame, text="Fecha Devolución (YYYY-MM-DD):").pack()
    entry_fecha_devolucion = ctk.CTkEntry(frame)
    entry_fecha_devolucion.pack()

    ctk.CTkButton(frame, text="Agregar Préstamo", command=agregar_prestamo).pack(pady=5)

    ctk.CTkButton(frame, text="Eliminar Préstamo", command=eliminar_prestamo).pack(pady=5)

    ctk.CTkButton(frame, text="Actualizar Préstamo", command=actualizar_prestamo).pack(pady=5)

    listbox = tk.Listbox(frame, width=100, height=12)
    listbox.pack()

    cargar_usuarios()
    cargar_copias_disponibles()
    cargar_lista()
