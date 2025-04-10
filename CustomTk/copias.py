import customtkinter as ctk
import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId
from db import db

copias_collection = db["copias"]
ediciones_collection = db["ediciones"]
libros_collection = db["libros"]

def crear_tab_copias(frame):
    def cargar_copias():
        listbox_copias.delete(0, tk.END)
        for copia in copias_collection.find():
            edicion = ediciones_collection.find_one({"_id": ObjectId(copia["edicion_id"])})
            if edicion:
                libro = libros_collection.find_one({"_id": ObjectId(edicion.get("libro_id"))})
                libro_nombre = libro["titulo"] if libro else "Libro desconocido"
                texto = f"Copia N°{copia['numero']} - {edicion['ISBN']} - {libro_nombre}"
            else:
                texto = f"Copia N°{copia['numero']} - Edición desconocida"
            listbox_copias.insert(tk.END, f"{copia['_id']} - {texto}")

    def agregar_copia():
        numero = entry_numero.get()
        edicion_text = combobox_ediciones.get()

        if not numero or not edicion_text:
            return

        edicion_id = edicion_text.split(" - ")[0]

        copias_collection.insert_one({
            "numero": int(numero),
            "edicion_id": edicion_id
        })
        cargar_copias()

    def actualizar_copia():
        seleccion = listbox_copias.curselection()
        if not seleccion:
            return
        item = listbox_copias.get(seleccion[0])
        copia_id = item.split(" - ")[0]

        numero = entry_numero.get()
        edicion_id = combobox_ediciones.get().split(" - ")[0]

        copias_collection.update_one(
            {"_id": ObjectId(copia_id)},
            {"$set": {"numero": int(numero), "edicion_id": edicion_id}}
        )
        cargar_copias()

    def eliminar_copia():
        seleccion = listbox_copias.curselection()
        if not seleccion:
            return
        item = listbox_copias.get(seleccion[0])
        copia_id = item.split(" - ")[0]

        copias_collection.delete_one({"_id": ObjectId(copia_id)})
        cargar_copias()

    def mostrar_copia(event):
        seleccion = listbox_copias.curselection()
        if not seleccion:
            return
        item = listbox_copias.get(seleccion[0])
        copia_id = item.split(" - ")[0]

        copia = copias_collection.find_one({"_id": ObjectId(copia_id)})
        edicion = ediciones_collection.find_one({"_id": ObjectId(copia["edicion_id"])})

        entry_numero.delete(0, ctk.END)
        entry_numero.insert(0, copia["numero"])

        if edicion:
            libro = libros_collection.find_one({"_id": ObjectId(edicion.get("libro_id"))})
            libro_nombre = libro["titulo"] if libro else "Libro desconocido"
            texto = f"{edicion['_id']} - {edicion['ISBN']} - {libro_nombre}"
            combobox_ediciones.set(texto)

    ctk.CTkLabel(frame, text="Número de Copia:").pack()
    entry_numero = ctk.CTkEntry(frame)
    entry_numero.pack()

    ctk.CTkLabel(frame, text="Edición:").pack()
    combobox_ediciones = ctk.CTkComboBox(frame, values=[])
    combobox_ediciones.pack()

    def cargar_ediciones():
        valores = []
        for ed in ediciones_collection.find():
            libro = libros_collection.find_one({"_id": ObjectId(ed.get("libro_id"))}) if ed.get("libro_id") else None
            libro_nombre = libro["titulo"] if libro else "Libro desconocido"
            valores.append(f"{ed['_id']} - {ed['ISBN']} - {libro_nombre}")
        combobox_ediciones.configure(values=valores)
        if valores:
            combobox_ediciones.set(valores[0])

    cargar_ediciones()

    ctk.CTkButton(frame, text="Agregar", command=agregar_copia).pack()
    ctk.CTkButton(frame, text="Actualizar", command=actualizar_copia).pack()
    ctk.CTkButton(frame, text="Eliminar", command=eliminar_copia).pack()

    listbox_copias = tk.Listbox(frame, width=80, height=10)
    listbox_copias.pack()
    listbox_copias.bind("<<ListboxSelect>>", mostrar_copia)

    cargar_copias()
