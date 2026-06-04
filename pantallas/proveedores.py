import tkinter as tk
from tkinter import ttk, messagebox
from utilidades.archivos import (crear_archivo, leer_registros, guardar_registros)

ARCHIVO = "datos/proveedores.txt"

def leer_proveedores():
    return leer_registros(ARCHIVO)

def guardar_proveedores(proveedores):
    guardar_registros(ARCHIVO, proveedores)

def limpiar_campos():
    identificador.set("")
    razon_social.set("")
    cuit.set("")
    direccion.set("")
    telefono.set("")
    email.set("")
    estado.set("ACTIVO")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for proveedor in leer_proveedores():
        tabla.insert("", "end", values=proveedor)


def validar_campos(incluir_identificador=True):

    if incluir_identificador:
        if identificador.get() == "":
            messagebox.showwarning("Atención", "Debe completar el Identificador.")
            return False

        if not identificador.get().isdigit():
            messagebox.showwarning("Atención", "El Identificador debe ser numérico.")
            return False

    if razon_social.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar la Razón Social.")
        return False

    if cuit.get() == "":
        messagebox.showwarning("Atención", "Debe completar el CUIT.")
        return False

    if not cuit.get().isdigit():
        messagebox.showwarning("Atención", "El CUIT debe ser numérico.")
        return False

    if direccion.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar la Dirección.")
        return False

    if telefono.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el Teléfono.")
        return False

    if email.get().strip() == "":
        messagebox.showwarning("Atención", "Debe completar el Email.")
        return False

    return True


def alta_proveedor():

    if not validar_campos(True):
        return

    proveedores = leer_proveedores()

    for proveedor in proveedores:
        if proveedor[0] == identificador.get():
            messagebox.showerror("Error", "El identificador ya existe.")
            return

    nuevo = [
        identificador.get(),
        razon_social.get().strip(),
        cuit.get(),
        direccion.get().strip(),
        telefono.get().strip(),
        email.get().strip(),
        estado.get()
    ]

    proveedores.append(nuevo)

    guardar_proveedores(proveedores)
    cargar_tabla()
    limpiar_campos()

    messagebox.showinfo("Alta", "Proveedor dado de alta correctamente.")


def baja_proveedor():

    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador.")
        return

    if not identificador.get().isdigit():
        messagebox.showwarning("Atención", "El Identificador debe ser numérico.")
        return

    proveedores = leer_proveedores()
    encontrado = False

    for proveedor in proveedores:
        if proveedor[0] == identificador.get():
            proveedor[6] = "BAJA"
            encontrado = True

    guardar_proveedores(proveedores)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Baja", "Proveedor dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Proveedor no encontrado.")


def modificar_proveedor():

    if identificador.get() == "":
        messagebox.showwarning("Atención", "Ingrese el Identificador.")
        return

    if not validar_campos(True):
        return

    proveedores = leer_proveedores()
    encontrado = False

    for proveedor in proveedores:
        if proveedor[0] == identificador.get():

            proveedor[1] = razon_social.get().strip()
            proveedor[2] = cuit.get()
            proveedor[3] = direccion.get().strip()
            proveedor[4] = telefono.get().strip()
            proveedor[5] = email.get().strip()
            proveedor[6] = estado.get()

            encontrado = True

    guardar_proveedores(proveedores)
    cargar_tabla()

    if encontrado:
        messagebox.showinfo("Modificación", "Proveedor modificado correctamente.")
    else:
        messagebox.showerror("Error", "Proveedor no encontrado.")


def seleccionar_proveedor(event):

    seleccionado = tabla.focus()

    if seleccionado:

        valores = tabla.item(seleccionado, "values")

        identificador.set(valores[0])
        razon_social.set(valores[1])
        cuit.set(valores[2])
        direccion.set(valores[3])
        telefono.set(valores[4])
        email.set(valores[5])
        estado.set(valores[6])


# ---------------- VENTANA ---------------- #

def abrir_proveedores():
    global ventana
    global tabla

    global identificador
    global razon_social
    global cuit
    global direccion
    global telefono
    global email
    global estado

    ventana = tk.Toplevel()
    ventana.title("Gestión de Proveedores")
    ventana.geometry("1050x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    # Variables
    identificador = tk.StringVar()
    razon_social = tk.StringVar()
    cuit = tk.StringVar()
    direccion = tk.StringVar()
    telefono = tk.StringVar()
    email = tk.StringVar()
    estado = tk.StringVar(value="ACTIVO")

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE PROVEEDORES",
        font=("Arial", 22, "bold"),
        bg="#f4f6fa",
        fg="#172033"
    )
    titulo.pack(pady=15)

    frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20)
    frame_form.place(x=30, y=80, width=390, height=450)

    tk.Label(
        frame_form,
        text="Datos del proveedor",
        font=("Arial", 14, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=identificador, width=30).grid(row=1, column=1, pady=5)

    tk.Label(frame_form, text="Razón Social:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=razon_social, width=30).grid(row=2, column=1, pady=5)

    tk.Label(frame_form, text="CUIT:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=cuit, width=30).grid(row=3, column=1, pady=5)

    tk.Label(frame_form, text="Dirección:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=direccion, width=30).grid(row=4, column=1, pady=5)

    tk.Label(frame_form, text="Teléfono:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=telefono, width=30).grid(row=5, column=1, pady=5)

    tk.Label(frame_form, text="Email:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=email, width=30).grid(row=6, column=1, pady=5)

    tk.Label(frame_form, text="Estado:", bg="white").grid(row=7, column=0, sticky="w", pady=5)

    ttk.Combobox(
        frame_form,
        textvariable=estado,
        values=["ACTIVO", "BAJA"],
        state="readonly",
        width=27
    ).grid(row=7, column=1, pady=5)

    tk.Button(
        frame_form,
        text="Alta",
        width=12,
        bg="#16A34A",
        fg="white",
        command=alta_proveedor
    ).grid(row=8, column=0, pady=15)

    tk.Button(
        frame_form,
        text="Modificar",
        width=12,
        bg="#2563EB",
        fg="white",
        command=modificar_proveedor
    ).grid(row=8, column=1, pady=15)

    tk.Button(
        frame_form,
        text="Baja",
        width=12,
        bg="#DC2626",
        fg="white",
        command=baja_proveedor
    ).grid(row=9, column=0, pady=5)

    tk.Button(
        frame_form,
        text="Limpiar",
        width=12,
        bg="#6B7280",
        fg="white",
        command=limpiar_campos
    ).grid(row=9, column=1, pady=5)

    # Tabla

    frame_tabla = tk.Frame(ventana, bg="white")
    frame_tabla.place(x=450, y=80, width=560, height=420)

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "razon_social", "cuit", "direccion", "telefono", "email", "estado"),
        show="headings"
    )

    tabla.heading("id", text="ID")
    tabla.heading("razon_social", text="Razón Social")
    tabla.heading("cuit", text="CUIT")
    tabla.heading("direccion", text="Dirección")
    tabla.heading("telefono", text="Teléfono")
    tabla.heading("email", text="Email")
    tabla.heading("estado", text="Estado")

    tabla.column("id", width=60)
    tabla.column("razon_social", width=120)
    tabla.column("cuit", width=100)
    tabla.column("direccion", width=120)
    tabla.column("telefono", width=100)
    tabla.column("email", width=150)
    tabla.column("estado", width=80)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scrollbar.set)

    scrollbar.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    tabla.bind("<<TreeviewSelect>>", seleccionar_proveedor)

    tk.Button(
        ventana,
        text="Salir",
        width=15,
        bg="#111827",
        fg="white",
        command=ventana.destroy
    ).place(x=900, y=510)

    cargar_tabla()