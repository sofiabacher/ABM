import tkinter as tk
from tkinter import ttk, messagebox

from utilidades.archivos import (crear_archivo, leer_registros, guardar_registros)
from utilidades.base_crud import BaseCRUD
from utilidades.base_pantalla import BasePantalla

# ----------------- ARCHIVO -----------------

ARCHIVO = "datos/clientes.txt"

def leer_clientes():
    return leer_registros(ARCHIVO)

def guardar_clientes(clientes):
    guardar_registros(ARCHIVO, clientes)


# ---------------- VENTANA -----------------

ui = BasePantalla(ventana, "GESTIÓN DE CLIENTES", ancho_tabla=470)
ui.crear_titulo()
form = ui.crear_contenedor_form()
ui.crear_contenedor_tabla()
tabla = ui.crear_tabla(["id", "nombre", "apellido", "dni", "direccion", "estado"])


# ---------------- VARIABLES ---------------

identificador = tk.StringVar()
nombre = tk.StringVar()
apellido = tk.StringVar()
dni = tk.StringVar()
direccion = tk.StringVar()
estado = tk.StringVar(value="ACTIVO") 


# -------------- FUNCIONES UI -------------

def cargar_tabla(datos=None):
    ui.limpiar_tabla()

    if datos is None:
        datos = leer_clientes()
    
    for cliente in datos:
        tabla.insert("", "end", values=cliente)

def limpiar_campos():
    identificador.set("")
    nombre.set("")
    apellido.set("")
    dni.set("")
    direccion.set("")
    estado.set("ACTIVO")

def seleccionar(event):
    seleccion = tabla.focus()
    if seleccion:
        v = tabla.item(seleccion, "values")
        
        identificador.set(v[0])
        nombre.set(v[1])
        apellido.set(v[2])
        dni.set(v[3])
        direccion.set(v[4])
        estado.set(v[5])

# ---------------- CRUD --------------

crud = BaseCrud(
    leer_clientes,
    guardar_clientes,
    cargar_tabla,
    limpiar_campos
)

def alta():
    nuevo = [
        identificador.get(),
        nombre.get().strip(),
        apellido.get().strip(),
        dni.get(),
        direccion.get().strip(),
        estado.get()
    ]

    resultado = crud.alta(nuevo, identificador.get())
    
    if resultado == "ERROR_DUPLICADO":
        messagebox.showerror("Error", "El ID ya existe")
    else:
        messagebox.showinfo("OK", "Cliente agregado correctamente")

def baja():
    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese ID")
        return

    ok = crud.baja(identificador.get())

    if ok:
        messagebox.showinfo("OK", "Cliente dado de baja")
    else:
        messagebox.showerror("Error", "No encontrado")

def modificar():
    nuevo = [
        identificador.get(),
        nombre.get().strip(),
        apellido.get().strip(),
        dni.get(),
        direccion.get().strip(),
        estado.get()
    ]

    ok = crud.modificar(identificador.get(), nuevo)

    if ok:
        messagebox.showinfo("OK", "Cliente modificado")
    else:
        messagebox.showerror("Error", "No encontrado")


# ----------- FORM ----------------------

tk.Label(form, text="Datos del cliente", bg="white",
    font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(form, text="ID:", bg="white").grid(row=1, column=0, sticky="w")
tk.Entry(form, textvariable=identificador).grid(row=1, column=1)

tk.Label(form, text="Nombre:", bg="white").grid(row=2, column=0, sticky="w")
tk.Entry(form, textvariable=nombre).grid(row=2, column=1)

tk.Label(form, text="Apellido:", bg="white").grid(row=3, column=0, sticky="w")
tk.Entry(form, textvariable=apellido).grid(row=3, column=1)

tk.Label(form, text="DNI:", bg="white").grid(row=4, column=0, sticky="w")
tk.Entry(form, textvariable=dni).grid(row=4, column=1)

tk.Label(form, text="Dirección:", bg="white").grid(row=5, column=0, sticky="w")
tk.Entry(form, textvariable=direccion).grid(row=5, column=1)

tk.Label(form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w")

ttk.Combobox(
    form, 
    textvariable=estado,
    values=["ACTIVO", "BAJA"],
    state="readonly",
    width=27
).grid(row=6, column=1)


# --------- BOTONES --------------

tk.Button(form, text="Alta", bg="#16A34A", fg="white", command=alta).grid(row=7, column=0, pady=10)
tk.Button(form, text="Modificar", bg="#2563EB", fg="white", command=modificar).grid(row=7, column=1, pady=10)
tk.Button(form, text="Baja", bg="#DC2626", fg="white", command=baja).grid(row=8, column=0)
tk.Button(form, text="Limpiar", bg="#6B7280", fg="white", command=limpiar_campos).grid(row=8, column=1)


# -------------------------------

tabla.bind("<<TreeviewSelect>>", seleccionar)
cargar_tabla()






def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for cliente in leer_clientes():
        tabla.insert("", "end", values=cliente)


def validar_campos(incluir_identificador=True):
    """Valida todos los campos del formulario. Retorna True si son válidos."""

    if incluir_identificador:
        if identificador.get() == "":
            messagebox.showwarning("Atención", "Debe completar el campo Identificador.")
            return False
        
        if not identificador.get().isdigit():
            messagebox.showwarning("Atención", "El Identificador debe ser numérico.")
            return False

    if nombre.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Nombre.")
        return False

    if apellido.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Apellido.")
        return False

    if dni.get() == "":
        messagebox.showwarning("Atención", "Debe completar el campo DNI.")
        return False
    if not dni.get().isdigit():
        messagebox.showwarning("Atención", "El DNI debe ser numérico.")
        return False

    if direccion.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el campo Dirección.")
        return False

    return True


def alta_cliente():
    if not validar_campos(incluir_identificador=True):
        return

    clientes = leer_clientes()

    for cliente in clientes:
        if cliente[0] == identificador.get():
            messagebox.showerror("Error", "El identificador ya existe.")
            return

    nuevo = [
        identificador.get(),
        nombre.get().strip(),
        apellido.get().strip(),
        dni.get(),
        direccion.get().strip(),
        estado.get()
    ]

    clientes.append(nuevo)
    guardar_clientes(clientes)
    cargar_tabla()
    limpiar_campos()

    messagebox.showinfo("Alta", "Cliente dado de alta correctamente.")


def baja_cliente():
    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador del cliente.")
        return
    if not identificador.get().isdigit():
        messagebox.showwarning("Atención", "El Identificador debe ser numérico.")
        return

    clientes = leer_clientes()
    encontrado = False

    for cliente in clientes:
        if cliente[0] == identificador.get():
            cliente[5] = "BAJA"
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Baja", "Cliente dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")


def modificar_cliente():
    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador del cliente.")
        return

    if not validar_campos(incluir_identificador=True):
        return

    clientes = leer_clientes()
    encontrado = False

    for cliente in clientes:
        if cliente[0] == identificador.get():
            cliente[1] = nombre.get().strip()
            cliente[2] = apellido.get().strip()
            cliente[3] = dni.get()
            cliente[4] = direccion.get().strip()
            cliente[5] = estado.get()
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Modificación", "Cliente modificado correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")


def seleccionar_cliente(event):
    seleccionado = tabla.focus()

    if seleccionado:
        valores = tabla.item(seleccionado, "values")

        identificador.set(valores[0])
        nombre.set(valores[1])
        apellido.set(valores[2])
        dni.set(valores[3])
        direccion.set(valores[4])
        estado.set(valores[5])


# Ventana principal
def abrir_clientes():
    global ventana
    global tabla

    global identificador
    global nombre
    global apellido
    global dni
    global direccion
    global estado

    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("950x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    # Variables
    identificador = tk.StringVar()
    nombre = tk.StringVar()
    apellido = tk.StringVar()
    dni = tk.StringVar()
    direccion = tk.StringVar()
    estado = tk.StringVar(value="ACTIVO")

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE CLIENTES",
        font=("Arial", 22, "bold"),
        bg="#f4f6fa",
        fg="#172033"
    )
    titulo.pack(pady=15)

    frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20)
    frame_form.place(x=30, y=80, width=390, height=420)

    tk.Label(
        frame_form,
        text="Datos del cliente",
        font=("Arial", 14, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=identificador, width=30).grid(row=1, column=1, pady=5)

    tk.Label(frame_form, text="Nombre:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=nombre, width=30).grid(row=2, column=1, pady=5)

    tk.Label(frame_form, text="Apellido:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=apellido, width=30).grid(row=3, column=1, pady=5)

    tk.Label(frame_form, text="DNI:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=dni, width=30).grid(row=4, column=1, pady=5)

    tk.Label(frame_form, text="Dirección:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=direccion, width=30).grid(row=5, column=1, pady=5)

    tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
    ttk.Combobox(
        frame_form,
        textvariable=estado,
        values=["ACTIVO", "BAJA"],
        state="readonly",
        width=27
    ).grid(row=6, column=1, pady=5)

    # Botones 
    tk.Button(
        frame_form, text="Alta", width=12,
        bg="#16A34A", fg="white", command=alta_cliente
    ).grid(row=7, column=0, pady=15)

    tk.Button(
        frame_form, text="Modificar", width=12,
        bg="#2563EB", fg="white", command=modificar_cliente
    ).grid(row=7, column=1, pady=15)

    tk.Button(
        frame_form, text="Baja", width=12,
        bg="#DC2626", fg="white", command=baja_cliente
    ).grid(row=8, column=0, pady=5)

    tk.Button(
        frame_form, text="Limpiar", width=12,
        bg="#6B7280", fg="white", command=limpiar_campos
    ).grid(row=8, column=1, pady=5)

    # Tabla 
    frame_tabla = tk.Frame(ventana, bg="white")
    frame_tabla.place(x=450, y=80, width=470, height=420)

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("identificador", "nombre", "apellido", "dni", "direccion", "estado"),
        show="headings"
    )

    tabla.heading("identificador", text="Identificador")
    tabla.heading("nombre",        text="Nombre")
    tabla.heading("apellido",      text="Apellido")
    tabla.heading("dni",           text="DNI")
    tabla.heading("direccion",     text="Dirección")
    tabla.heading("estado",        text="Estado")

    tabla.column("identificador", width=80)
    tabla.column("nombre",        width=80)
    tabla.column("apellido",      width=80)
    tabla.column("dni",           width=75)
    tabla.column("direccion",     width=100)
    tabla.column("estado",        width=60)

    # Scrollbar horizontal para la tabla
    scrollbar = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scrollbar.set)
    scrollbar.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)
    tabla.bind("<<TreeviewSelect>>", seleccionar_cliente)


    tk.Button(
        ventana,
        text="Salir",
        width=15,
        bg="#111827",
        fg="white",
        command=ventana.destroy
    ).place(x=800, y=510)

    cargar_tabla()