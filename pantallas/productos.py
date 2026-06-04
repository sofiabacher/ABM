import tkinter as tk
from tkinter import ttk, messagebox
from utilidades.archivos import (crear_archivo, leer_registros, guardar_registros)

ARCHIVO = "datos/productos.txt"

def leer_productos():
    return leer_registros(ARCHIVO)

def guardar_productos(productos):
    guardar_registros(ARCHIVO, productos)

def limpiar_campos():
    identificador.set("")
    descripcion.set("")
    categoria.set("")
    precio.set("")
    talle.set("M")
    color.set("NEGRO")
    estado.set("ACTIVO")


def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for producto in leer_productos():
        tabla.insert("", "end", values=producto)


def validar_campos(incluir_id=True):
    if incluir_id:
        if identificador.get() == "":
            messagebox.showwarning("Atención", "Debe completar el Identificador.")
            return False

        if not identificador.get().isdigit():
            messagebox.showwarning("Atención", "El Identificador debe ser numérico.")
            return False

    if descripcion.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar la Descripción.")
        return False

    if categoria.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar la Categoría.")
        return False

    if precio.get() == "":
        messagebox.showwarning("Atención", "Debe completar el Precio.")
        return False

    try:
        float(precio.get())
    except:
        messagebox.showwarning("Atención", "El Precio debe ser numérico.")
        return False

    return True


# -------------------------------- #

def alta_producto():
    if not validar_campos(True):
        return

    productos = leer_productos()

    for producto in productos:
        if producto[0] == identificador.get():
            messagebox.showerror("Error", "El identificador ya existe.")
            return

    nuevo = [
        identificador.get(),
        descripcion.get().strip(),
        categoria.get().strip(),
        precio.get(),
        talle.get(),
        color.get(),
        estado.get()
    ]

    productos.append(nuevo)

    guardar_productos(productos)
    cargar_tabla()
    limpiar_campos()

    messagebox.showinfo("Alta", "Producto dado de alta correctamente.")


def baja_producto():
    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador.")
        return

    productos = leer_productos()
    encontrado = False

    for producto in productos:
        if producto[0] == identificador.get():
            producto[6] = "BAJA"
            encontrado = True

    guardar_productos(productos)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Baja", "Producto dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")


def modificar_producto():
    if identificador.get() == "":
        messagebox.showwarning("Atención","Ingrese el Identificador.")
        return

    if not validar_campos(True):
        return

    productos = leer_productos()
    encontrado = False

    for producto in productos:
        if producto[0] == identificador.get():
            producto[1] = descripcion.get().strip()
            producto[2] = categoria.get().strip()
            producto[3] = precio.get()
            producto[4] = talle.get()
            producto[5] = color.get()
            producto[6] = estado.get()

            encontrado = True

    guardar_productos(productos)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Modificación","Producto modificado correctamente.")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")


def seleccionar_producto(event):
    seleccionado = tabla.focus()

    if seleccionado:
        valores = tabla.item(seleccionado, "values")

        identificador.set(valores[0])
        descripcion.set(valores[1])
        categoria.set(valores[2])
        precio.set(valores[3])
        talle.set(valores[4])
        color.set(valores[5])
        estado.set(valores[6])


# -------------------------------- #

def abrir_productos():
    global ventana
    global tabla

    global identificador
    global descripcion
    global categoria
    global precio
    global talle
    global color
    global estado

    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("1050x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    identificador = tk.StringVar()
    descripcion = tk.StringVar()
    categoria = tk.StringVar()
    precio = tk.StringVar()
    talle = tk.StringVar(value="M")
    color = tk.StringVar(value="NEGRO")
    estado = tk.StringVar(value="ACTIVO")

    tk.Label(
        ventana,
        text="GESTIÓN DE PRODUCTOS",
        font=("Arial", 22, "bold"),
        bg="#f4f6fa",
        fg="#172033"
    ).pack(pady=15)

    frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20)
    frame_form.place( x=30, y=80, width=390, height=450)

    tk.Label(
        frame_form,
        text="Datos del producto",
        font=("Arial", 14, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w")
    tk.Entry(frame_form, textvariable=identificador, width=30).grid(row=1, column=1)

    tk.Label(frame_form, text="Descripción:", bg="white").grid(row=2, column=0, sticky="w")
    tk.Entry(frame_form, textvariable=descripcion, width=30).grid(row=2, column=1)

    tk.Label(frame_form, text="Categoría:", bg="white").grid(row=3, column=0, sticky="w")
    tk.Entry(frame_form, textvariable=categoria, width=30).grid(row=3, column=1)

    tk.Label(frame_form, text="Precio:", bg="white").grid(row=4, column=0, sticky="w")
    tk.Entry(frame_form, textvariable=precio, width=30).grid(row=4, column=1)

    tk.Label(frame_form, text="Talle:", bg="white").grid(row=5, column=0, sticky="w")

    ttk.Combobox(
        frame_form,
        textvariable=talle,
        values=["XS", "S", "M", "L", "XL", "XXL"],
        state="readonly",
        width=27
    ).grid(row=5, column=1)

    tk.Label(frame_form, text="Color:", bg="white").grid(row=6, column=0, sticky="w")

    ttk.Combobox(
        frame_form,
        textvariable=color,
        values=["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"],
        state="readonly",
        width=27
    ).grid(row=6, column=1)

    tk.Label(frame_form, text="Estado:", bg="white").grid(row=7, column=0, sticky="w")

    ttk.Combobox(
        frame_form,
        textvariable=estado,
        values=["ACTIVO", "BAJA"],
        state="readonly",
        width=27
    ).grid(row=7, column=1)

    tk.Button(
        frame_form,
        text="Alta",
        width=12,
        bg="#16A34A",
        fg="white",
        command=alta_producto
    ).grid(row=8, column=0, pady=15)

    tk.Button(
        frame_form,
        text="Modificar",
        width=12,
        bg="#2563EB",
        fg="white",
        command=modificar_producto
    ).grid(row=8, column=1, pady=15)

    tk.Button(
        frame_form,
        text="Baja",
        width=12,
        bg="#DC2626",
        fg="white",
        command=baja_producto
    ).grid(row=9, column=0)

    tk.Button(
        frame_form,
        text="Limpiar",
        width=12,
        bg="#6B7280",
        fg="white",
        command=limpiar_campos
    ).grid(row=9, column=1)


    frame_tabla = tk.Frame(ventana, bg="white")

    frame_tabla.place(x=450, y=80, width=560, height=420)

    tabla = ttk.Treeview(
        frame_tabla,
        columns=(
            "id",
            "descripcion",
            "categoria",
            "precio",
            "talle",
            "color",
            "estado"
        ),
        show="headings"
    )

    tabla.heading("id", text="ID")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("categoria", text="Categoría")
    tabla.heading("precio", text="Precio")
    tabla.heading("talle", text="Talle")
    tabla.heading("color", text="Color")
    tabla.heading("estado", text="Estado")

    tabla.column("id", width=50)
    tabla.column("descripcion", width=120)
    tabla.column("categoria", width=100)
    tabla.column("precio", width=80)
    tabla.column("talle", width=60)
    tabla.column("color", width=90)
    tabla.column("estado", width=70)

    scrollbar = ttk.Scrollbar( frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure( xscrollcommand=scrollbar.set)

    scrollbar.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    tabla.bind( "<<TreeviewSelect>>", seleccionar_producto)

    tk.Button(
        ventana,
        text="Salir",
        width=15,
        bg="#111827",
        fg="white",
        command=ventana.destroy
    ).place(x=900, y=510)

    cargar_tabla()
