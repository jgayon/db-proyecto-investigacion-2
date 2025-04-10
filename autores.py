# autores.py
import customtkinter as ctk
from tkinter import messagebox
from pymongo import MongoClient
from bson import ObjectId
from db import db

autor_nombre = None
lista_autores = None
autor_id_seleccionado = None

def crear_autor():
    if autor_nombre.get():
        db.autores.insert_one({"nombre": autor_nombre.get()})
        autor_nombre.set("")
        actualizar_autores()

def actualizar_autor():
    global autor_id_seleccionado
    if autor_id_seleccionado:
        db.autores.update_one(
            {"_id": autor_id_seleccionado},
            {"$set": {"nombre": autor_nombre.get()}}
        )
        autor_nombre.set("")
        actualizar_autores()

def eliminar_autor():
    global autor_id_seleccionado
    if autor_id_seleccionado:
        db.autores.delete_one({"_id": autor_id_seleccionado})
        autor_nombre.set("")
        actualizar_autores()

def seleccionar_autor(event):
    global autor_id_seleccionado
    try:
        linea = lista_autores.get("insert linestart", "insert lineend")
        autor_id = linea.split(" - ")[0]
        autor = db.autores.find_one({"_id": ObjectId(autor_id)})
        if autor:
            autor_id_seleccionado = autor["_id"]
            autor_nombre.set(autor["nombre"])
    except:
        pass

def actualizar_autores():
    lista_autores.delete("0.0", "end")
    for autor in db.autores.find():
        lista_autores.insert("end", f"{autor['_id']} - {autor['nombre']}\n")

def crear_tab_autores(tab):
    global autor_nombre, lista_autores

    autor_nombre = ctk.StringVar()

    ctk.CTkLabel(tab, text="Nombre del autor:").pack(pady=(10, 2))
    ctk.CTkEntry(tab, textvariable=autor_nombre).pack(pady=2)

    ctk.CTkButton(tab, text="Crear autor", command=crear_autor).pack(pady=4)

    lista_autores = ctk.CTkTextbox(tab, height=200)
    lista_autores.pack(fill="both", expand=True, pady=(10, 4))
    lista_autores.bind("<ButtonRelease-1>", seleccionar_autor)

    ctk.CTkButton(tab, text="Actualizar autor", command=actualizar_autor).pack(pady=4)
    ctk.CTkButton(tab, text="Eliminar autor", command=eliminar_autor).pack(pady=4)

    actualizar_autores()
