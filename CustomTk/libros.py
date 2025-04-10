import customtkinter as ctk
from tkinter import messagebox
from bson import ObjectId
from db import db

titulo_libro = None
lista_libros = None
libro_id_seleccionado = None
autor_id_manual = None
autor_seleccionado = None

def crear_libro():
    id_manual = autor_id_manual.get().strip()
    id_desde_menu = autor_seleccionado.get().split(" - ")[0]

    if titulo_libro.get():
        try:
            autor_id_final = ObjectId(id_manual if id_manual else id_desde_menu)

            db.libros.insert_one({
                "titulo": titulo_libro.get(),
                "autores": [autor_id_final]  # CAMBIO AQUÍ
            })
            titulo_libro.set("")
            autor_id_manual.set("")
            actualizar_libros()
        except:
            messagebox.showerror("Error", "ID de autor inválido.")

def actualizar_libro():
    global libro_id_seleccionado
    if libro_id_seleccionado:
        id_manual = autor_id_manual.get().strip()
        id_desde_menu = autor_seleccionado.get().split(" - ")[0]

        try:
            autor_id_final = ObjectId(id_manual if id_manual else id_desde_menu)

            db.libros.update_one(
                {"_id": libro_id_seleccionado},
                {
                    "$set": {
                        "titulo": titulo_libro.get(),
                        "autores": [autor_id_final]  # CAMBIO AQUÍ
                    }
                }
            )
            titulo_libro.set("")
            autor_id_manual.set("")
            actualizar_libros()
        except:
            messagebox.showerror("Error", "ID de autor inválido.")

def eliminar_libro():
    global libro_id_seleccionado
    if libro_id_seleccionado:
        db.libros.delete_one({"_id": libro_id_seleccionado})
        titulo_libro.set("")
        autor_id_manual.set("")
        actualizar_libros()

def seleccionar_libro(event):
    global libro_id_seleccionado
    try:
        linea = lista_libros.get("insert linestart", "insert lineend")
        libro_id = linea.split(" - ")[0]
        libro = db.libros.find_one({"_id": ObjectId(libro_id)})
        if libro:
            libro_id_seleccionado = libro["_id"]
            titulo_libro.set(libro["titulo"])
    except:
        pass

def actualizar_libros():
    lista_libros.delete("0.0", "end")
    for libro in db.libros.find():
        autor_nombres = []
        for aid in libro.get("autores", []):  # CAMBIO AQUÍ
            autor = db.autores.find_one({"_id": aid})
            if autor:
                autor_nombres.append(autor["nombre"])
        autores_str = ", ".join(autor_nombres)
        lista_libros.insert("end", f"{libro['_id']} - {libro['titulo']} (Autores: {autores_str})\n")

def crear_tab_libros(tab):
    global titulo_libro, lista_libros, autor_id_manual, autor_seleccionado

    titulo_libro = ctk.StringVar()
    autor_id_manual = ctk.StringVar()

    ctk.CTkLabel(tab, text="Título del libro:").pack(pady=(10, 2))
    ctk.CTkEntry(tab, textvariable=titulo_libro).pack(pady=2)

    # Frame para selección de autor
    frame_autor = ctk.CTkFrame(tab)
    frame_autor.pack(pady=5)

    # Opción 1: Menú de nombres
    autores = list(db.autores.find())
    autor_nombres = [f"{autor['_id']} - {autor['nombre']}" for autor in autores]
    autor_seleccionado = ctk.StringVar(value=autor_nombres[0] if autor_nombres else "")

    ctk.CTkLabel(frame_autor, text="Autor:").grid(row=0, column=0, padx=5)
    ctk.CTkOptionMenu(frame_autor, values=autor_nombres, variable=autor_seleccionado).grid(row=1, column=0, padx=5)

    # Opción 2: ID manual
    ctk.CTkLabel(frame_autor, text="o ID del Autor:").grid(row=0, column=1, padx=5)
    ctk.CTkEntry(frame_autor, textvariable=autor_id_manual).grid(row=1, column=1, padx=5)

    # Botones
    ctk.CTkButton(tab, text="Crear libro", command=crear_libro).pack(pady=4)

    lista_libros = ctk.CTkTextbox(tab, height=200)
    lista_libros.pack(fill="both", expand=True, pady=(10, 4))
    lista_libros.bind("<ButtonRelease-1>", seleccionar_libro)

    ctk.CTkButton(tab, text="Actualizar libro", command=actualizar_libro).pack(pady=4)
    ctk.CTkButton(tab, text="Eliminar libro", command=eliminar_libro).pack(pady=4)

    actualizar_libros()
