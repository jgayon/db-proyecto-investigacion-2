import customtkinter as ctk
import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId
from db import db

# Conexiones a colecciones
copias_collection = db["copias"]
ediciones_collection = db["ediciones"]
libros_collection = db["libros"]
autores_collection = db["autores"]
usuarios_collection = db["usuarios"]
prestamos_collection = db["prestamos"]

def crear_tab_consultas(tab):
    # Frame superior para entradas y botones
    frame_selector = ctk.CTkFrame(tab)
    frame_selector.pack(pady=10)

    # Campo de entrada para el RUT (consulta 2)
    ctk.CTkLabel(frame_selector, text="RUT del usuario para Consulta 2:").grid(row=0, column=0, padx=10)
    entry_rut = ctk.CTkEntry(frame_selector)
    entry_rut.grid(row=0, column=1, padx=10)

    # Caja de texto para mostrar resultados
    resultado_box = tk.Listbox(tab, height=20, width=100)
    resultado_box.pack(pady=10)

    # Consulta 1: Listar copias con detalles
    def consulta_1(lista_resultados):
        lista_resultados.delete(0, tk.END)
        for copia in copias_collection.find():
            edicion = ediciones_collection.find_one({"_id": ObjectId(copia["edicion_id"])})
            if not edicion:
                continue
            libro = libros_collection.find_one({"_id": ObjectId(edicion["libro_id"])})
            if not libro:
                continue

            texto = f"Copia N°{copia['numero']}\n"
            texto += f" - Libro: {libro.get('titulo', 'desconocido')}\n"

            autores_ids = libro.get("autores", [])
            nombres_autores = []
            for autor_id in autores_ids:
                try:
                    if isinstance(autor_id, str):
                        autor_id = ObjectId(autor_id)
                    autor = autores_collection.find_one({"_id": autor_id})
                    if autor:
                        nombres_autores.append(autor["nombre"])
                except Exception as e:
                    print(f"Error al convertir autor_id: {autor_id} -> {e}")


            texto += " - Autores: " + ", ".join(nombres_autores) if nombres_autores else " Autores: Desconocidos"
            lista_resultados.insert(tk.END, texto)
            lista_resultados.insert(tk.END, "-" * 60)

    # Consulta 2: Buscar préstamos por RUT
    def consulta_2(lista_resultados, rut_usuario):
        lista_resultados.delete(0, tk.END)
        usuario = usuarios_collection.find_one({"rut": rut_usuario})
        if not usuario:
            lista_resultados.insert(tk.END, f"No se encontró usuario con RUT: {rut_usuario}")
            return

        texto = f"Libros prestados por {usuario['nombre']} (RUT: {rut_usuario}):"
        lista_resultados.insert(tk.END, texto)

        prestamos = prestamos_collection.find({"usuario_id": usuario["_id"]})
        encontrado = False
        for prestamo in prestamos:
            copia = copias_collection.find_one({"_id": ObjectId(prestamo["copia_id"])})
            if not copia:
                continue
            edicion = ediciones_collection.find_one({"_id": ObjectId(copia["edicion_id"])})
            if not edicion:
                continue
            libro = libros_collection.find_one({"_id": ObjectId(edicion["libro_id"])})
            if not libro:
                continue

            encontrado = True
            titulo = libro.get("titulo", "Título desconocido")
            lista_resultados.insert(tk.END, f"- {titulo} (Copia N°{copia['numero']})")

        if not encontrado:
            lista_resultados.insert(tk.END, "No tiene libros prestados.")

    # Botones para ejecutar consultas con parámetros
    ctk.CTkButton(
        frame_selector,
        text="Consulta 1: Copias con detalles",
        command=lambda: consulta_1(resultado_box)
    ).grid(row=1, column=0, pady=10, padx=10)

    ctk.CTkButton(
        frame_selector,
        text="Consulta 2: Libros prestados por usuario",
        command=lambda: consulta_2(resultado_box, entry_rut.get())
    ).grid(row=1, column=1, pady=10, padx=10)
