import tkinter as tk
from tkinter import ttk, messagebox

from utilidades.archivos import leer_registros, guardar_registros
from utilidades.base_crud import BaseCRUD
from utilidades.base_pantalla import BasePantalla

ARCHIVO = "datos/productos.txt"

def leer_productos():
    return leer_registros(ARCHIVO)

def guardar_productos(productos):
    guardar_registros(ARCHIVO, productos)

def abrir_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("1050x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    # ---------------- VARIABLES ----------------

    identificador = tk.StringVar()
    descripcion = tk.StringVar()
    categoria = tk.StringVar()
    precio = tk.StringVar()
    talle = tk.StringVar(value="M")
    color = tk.StringVar(value="NEGRO")
    estado = tk.StringVar(value="ACTIVO")

    # ---------------- UI BASE ----------------

    ui = BasePantalla(
        ventana,
        "GESTIÓN DE PRODUCTOS",
        ancho_tabla=560
    )

    ui.crear_titulo()
    ui.crear_contenedor_tabla()

    form = ui.crear_contenedor_form()

    tabla = ui.crear_tabla(
        ["id", "descripcion", "categoria", "precio", "talle","color", "estado"]
    )

    # -------------- FUNCIONES -------------

    def cargar_tabla(datos=None):
        ui.limpiar_tabla()

        if datos is None:
            datos = leer_productos()

        for producto in datos:
            tabla.insert("", "end", values=producto)

    def limpiar_campos():
        identificador.set("")
        descripcion.set("")
        categoria.set("")
        precio.set("")
        talle.set("M")
        color.set("NEGRO")
        estado.set("ACTIVO")

    def validar_campos():
        if not crud.validar_requerido(identificador.get(), "Identificador"):
            return False

        if not crud.validar_numerico(identificador.get(), "Identificador"):
            return False

        if not crud.validar_requerido(descripcion.get(), "Descripción"):
            return False

        if not crud.validar_requerido(categoria.get(), "Categoria"):
            return False

        if precio.get() == "":
            messagebox.showwarning("Atención", "Debe completar el Precio.")
            return False

        if not crud.validar_requerido(precio.get(), "Precio"):
            return False

        if not crud.validar_numerico(precio.get(), "Precio"):
            return False

        return True

    def seleccionar(event):
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

    # -------------- CRUD ------------------

    crud = BaseCRUD(
        leer_productos,
        guardar_productos,
        cargar_tabla,
        limpiar_campos
    )

    def alta():
        if not validar_campos():
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

        resultado = crud.alta(nuevo, identificador.get())

        if resultado == "OK":
            messagebox.showinfo("OK", "Cliente agregado correctamente")
            
        elif resultado == "ERROR_DUPLICADO":
            messagebox.showerror("Error", "El identificador ya existe")

    def baja():
        if not crud.validar_requerido(identificador.get(), "Identificador"):
            return

        ok = crud.baja(identificador.get())

        if ok:
            messagebox.showinfo("Baja", "Producto dado de baja correctamente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")


    def modificar():
        if not validar_campos(True):
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

        ok = crud.modificar(identificador.get(), nuevo)

        if ok:
            messagebox.showinfo("Modificación","Producto modificado correctamente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    # ------------- FORMULARIO -------------------

    tk.Label(
        form,
        text="Datos del producto",
        font=("Arial", 14, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w")
    tk.Entry(form, textvariable=identificador, width=30).grid(row=1, column=1)

    tk.Label(form, text="Descripción:", bg="white").grid(row=2, column=0, sticky="w")
    tk.Entry(form, textvariable=descripcion, width=30).grid(row=2, column=1)

    tk.Label(form, text="Categoría:", bg="white").grid(row=3, column=0, sticky="w")
    tk.Entry(form, textvariable=categoria, width=30).grid(row=3, column=1)

    tk.Label(form, text="Precio:", bg="white").grid(row=4, column=0, sticky="w")
    tk.Entry(form, textvariable=precio, width=30).grid(row=4, column=1)

    tk.Label(form, text="Talle:", bg="white").grid(row=5, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=talle,
        values=["XS", "S", "M", "L", "XL", "XXL"],
        state="readonly",
        width=27
    ).grid(row=5, column=1)

    tk.Label(form, text="Color:", bg="white").grid(row=6, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=color,
        values=["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"],
        state="readonly",
        width=27
    ).grid(row=6, column=1)

    tk.Label(form, text="Estado:", bg="white").grid(row=7, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=estado,
        values=["ACTIVO", "BAJA"],
        state="readonly",
        width=27
    ).grid(row=7, column=1)

    # ------------- BOTONES -------------------

    tk.Button(form, text="Alta", bg="#16A34A", fg="white", command=alta).grid(row=8, column=0, pady=15)
    tk.Button(form, text="Modificar", bg="#2563EB", fg="white", command=modificar).grid(row=8, column=1, pady=15)
    tk.Button(form, text="Baja", bg="#DC2626", fg="white",command=baja).grid(row=9, column=0)
    tk.Button(form, text="Limpiar", bg="#6B7280", fg="white", command=limpiar_campos).grid(row=9, column=1)

    # ------------- TABLA -------------------

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(
        ventana,
        text="Salir",
        width=15,
        bg="#111827",
        fg="white",
        command=ventana.destroy
    ).place(x=900, y=510)

    cargar_tabla()