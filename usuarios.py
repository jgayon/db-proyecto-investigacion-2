# usuarios.py
import customtkinter as ctk
import tkinter as tk
from pymongo import MongoClient
from tkinter import messagebox
from db import db

usuarios_collection = db["usuarios"]

def crear_tab_usuarios(frame):
    def cargar_usuarios():
        listbox_usuarios.delete(0, tk.END)
        for usuario in usuarios_collection.find():
            listbox_usuarios.insert(tk.END, f"{usuario['rut']} - {usuario['nombre']}")

    def agregar_usuario():
        rut = entry_rut.get()
        nombre = entry_nombre.get()
        if rut and nombre:
            if usuarios_collection.find_one({"rut": rut}):
                messagebox.showwarning("Advertencia", "El RUT ya existe.")
            else:
                usuarios_collection.insert_one({"rut": rut, "nombre": nombre})
                entry_rut.delete(0, ctk.END)
                entry_nombre.delete(0, ctk.END)
                cargar_usuarios()
        else:
            messagebox.showwarning("Advertencia", "Completa todos los campos.")

    def eliminar_usuario():
        seleccion = listbox_usuarios.curselection()
        if seleccion:
            item = listbox_usuarios.get(seleccion[0])
            rut = item.split(" - ")[0]
            usuarios_collection.delete_one({"rut": rut})
            cargar_usuarios()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un usuario.")

    def actualizar_usuario():
        seleccion = listbox_usuarios.curselection()
        if seleccion:
            item = listbox_usuarios.get(seleccion[0])
            rut_original = item.split(" - ")[0]
            nuevo_rut = entry_rut.get()
            nuevo_nombre = entry_nombre.get()
            if nuevo_rut and nuevo_nombre:
                usuarios_collection.update_one(
                    {"rut": rut_original},
                    {"$set": {"rut": nuevo_rut, "nombre": nuevo_nombre}}
                )
                cargar_usuarios()
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un usuario.")

    def cargar_datos_usuario(event):
        seleccion = listbox_usuarios.curselection()
        if seleccion:
            item = listbox_usuarios.get(seleccion[0])
            rut, nombre = item.split(" - ")
            entry_rut.delete(0, ctk.END)
            entry_nombre.delete(0, ctk.END)
            entry_rut.insert(0, rut)
            entry_nombre.insert(0, nombre)

    # Entradas
    ctk.CTkLabel(frame, text="RUT:").grid(row=0, column=0, padx=10, pady=5)
    entry_rut = ctk.CTkEntry(frame)
    entry_rut.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
    entry_nombre = ctk.CTkEntry(frame)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    # Botones
    ctk.CTkButton(frame, text="Agregar", command=agregar_usuario).grid(row=2, column=0, padx=10, pady=5)
    ctk.CTkButton(frame, text="Actualizar", command=actualizar_usuario).grid(row=2, column=1, padx=10, pady=5)
    ctk.CTkButton(frame, text="Eliminar", command=eliminar_usuario).grid(row=2, column=2, padx=10, pady=5)

    # Listbox (de tkinter)
    listbox_usuarios = tk.Listbox(frame, width=50, height=10)
    listbox_usuarios.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    listbox_usuarios.bind("<<ListboxSelect>>", cargar_datos_usuario)

    cargar_usuarios()
