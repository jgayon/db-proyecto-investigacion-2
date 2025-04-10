# app.py
import customtkinter as ctk
from autores import crear_tab_autores
from consultas import crear_tab_consultas
from copias import crear_tab_copias
from libros import crear_tab_libros
from ediciones import crear_tab_ediciones
from prestamos import crear_tab_prestamos
from usuarios import crear_tab_usuarios


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sistema de Biblioteca")
root.geometry("900x600")

notebook = ctk.CTkTabview(master=root, width=900, height=580)
notebook.pack(padx=20, pady=20, fill="both", expand=True)

# Crear pestañas
tab_autores = notebook.add("Autores")
crear_tab_autores(tab_autores)

tab_libros = notebook.add("Libros")
crear_tab_libros(tab_libros)

tab_edicion = notebook.add("Ediciones")
crear_tab_ediciones(tab_edicion)

tab_copias = notebook.add("Copias")
crear_tab_copias(tab_copias)

tab_usuarios = notebook.add("Usuarios")
crear_tab_usuarios(tab_usuarios)

tab_prestamos = notebook.add("Préstamos")
crear_tab_prestamos(tab_prestamos)

tab_consultas = notebook.add("Consultas")
crear_tab_consultas(tab_consultas)

root.mainloop()
