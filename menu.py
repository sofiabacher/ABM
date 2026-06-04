import tkinter as tk
from tkinter import messagebox
from pantallas import (clientes, productos, proveedores)

def abrir_clientes():
    clientes.abrir_clientes()

def abrir_proveedores():
    proveedores.abrir_proveedores()

def abrir_productos():
    productos.abrir_productos()

#def abrir_facturacion():


def salir():
    respuesta = messagebox.askyesno("Salir", "¿Desea salir del sistema?")
    if respuesta:
        ventana_menu.destroy()


# ---------------- MENU PRINCIPAL ------------

ventana_menu = tk.Tk()
ventana_menu.title("Sistema principal")
ventana_menu.geometry("400x400")
ventana_menu.configure(bg="#f4f6fa")
ventana_menu.resizable(False, False)

tk.Label(
    ventana_menu,
    text="MENÚ PRINCIPAL",
    font=("Arial", 20, "bold"),
    bg="#f4f6fa"
).pack(pady=30)

tk.Button(
    ventana_menu,
    text="Gestión de Clientes",
    width=25,
    command=abrir_clientes
).pack(pady=10)

tk.Button(
    ventana_menu,
    text="Gestión de Proveedores",
    width=25,
    command=abrir_proveedores
).pack(pady=10)

tk.Button(
    ventana_menu,
    text="Gestión de Productos",
    width=25,
    command=abrir_productos
).pack(pady=10)

tk.Button(
    ventana_menu,
    text="Facturación",
    width=25
    #command=abrir_facturacion
).pack(pady=10)

tk.Button(
    ventana_menu,
    text="Salir",
    width=25,
    bg="#DC2626",
    fg="white",
    command=salir
).pack(pady=20)

ventana_menu.mainloop()