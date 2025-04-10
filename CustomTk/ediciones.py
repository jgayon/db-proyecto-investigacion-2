import customtkinter as ctk
import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId
from db import db

ediciones_collection = db["ediciones"]
libros_collection = db["libros"]

def crear_tab_ediciones(frame):
    def cargar_ediciones():
        listbox.delete(0, tk.END)
        for edicion in ediciones_collection.find():
            libro_id = edicion.get("libro_id")
            if isinstance(libro_id, str):
                try:
                    libro_id = ObjectId(libro_id)
                except:
                    libro_id = None

            libro = libros_collection.find_one({"_id": libro_id}) if libro_id else None
            libro_titulo = libro["titulo"] if libro else "Libro desconocido"
            texto = f"{edicion['_id']} - ISBN: {edicion['ISBN']} - Idioma: {edicion['idioma']} - {libro_titulo}"
            listbox.insert(tk.END, texto)

    def agregar_edicion():
        isbn = entry_isbn.get()
        idioma = entry_idioma.get()
        libro_text = combobox_libros.get()

        if not isbn or not idioma or not libro_text:
            return

        libro_id = libro_text.split(" - ")[0]

        ediciones_collection.insert_one({
            "ISBN": isbn,
            "idioma": idioma,
            "libro_id": ObjectId(libro_id)
        })
        cargar_ediciones()

    def actualizar_edicion():
        seleccion = listbox.curselection()
        if not seleccion:
            return
        item = listbox.get(seleccion[0])
        edicion_id = item.split(" - ")[0]

        isbn = entry_isbn.get()
        idioma = entry_idioma.get()
        libro_id = combobox_libros.get().split(" - ")[0]

        ediciones_collection.update_one(
            {"_id": ObjectId(edicion_id)},
            {"$set": {
                "ISBN": isbn,
                "idioma": idioma,
                "libro_id": ObjectId(libro_id)
            }}
        )
        cargar_ediciones()

    def eliminar_edicion():
        seleccion = listbox.curselection()
        if not seleccion:
            return
        item = listbox.get(seleccion[0])
        edicion_id = item.split(" - ")[0]

        ediciones_collection.delete_one({"_id": ObjectId(edicion_id)})
        cargar_ediciones()

    def mostrar_edicion(event):
        seleccion = listbox.curselection()
        if not seleccion:
            return
        item = listbox.get(seleccion[0])
        edicion_id = item.split(" - ")[0]

        edicion = ediciones_collection.find_one({"_id": ObjectId(edicion_id)})

        libro_id = edicion.get("libro_id")
        if isinstance(libro_id, str):
            try:
                libro_id = ObjectId(libro_id)
            except:
                libro_id = None

        libro = libros_collection.find_one({"_id": libro_id}) if libro_id else None

        entry_isbn.delete(0, ctk.END)
        entry_isbn.insert(0, edicion["ISBN"])

        entry_idioma.delete(0, ctk.END)
        entry_idioma.insert(0, edicion["idioma"])

        if libro:
            combobox_libros.set(f"{libro['_id']} - {libro['titulo']}")

    ctk.CTkLabel(frame, text="ISBN:").pack()
    entry_isbn = ctk.CTkEntry(frame)
    entry_isbn.pack()

    ctk.CTkLabel(frame, text="Idioma:").pack()
    entry_idioma = ctk.CTkEntry(frame)
    entry_idioma.pack()

    ctk.CTkLabel(frame, text="Libro:").pack()
    combobox_libros = ctk.CTkComboBox(frame, values=[])
    combobox_libros.pack()

    def cargar_libros():
        libros = libros_collection.find()
        valores = [f"{libro['_id']} - {libro['titulo']}" for libro in libros]
        combobox_libros.configure(values=valores)
        if valores:
            combobox_libros.set(valores[0])

    cargar_libros()

    ctk.CTkButton(frame, text="Agregar", command=agregar_edicion).pack()
    ctk.CTkButton(frame, text="Actualizar", command=actualizar_edicion).pack()
    ctk.CTkButton(frame, text="Eliminar", command=eliminar_edicion).pack()

    listbox = tk.Listbox(frame, width=80, height=10)
    listbox.pack()
    listbox.bind("<<ListboxSelect>>", mostrar_edicion)

    cargar_ediciones()

