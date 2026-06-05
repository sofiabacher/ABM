import tkinter as tk
from tkinter import ttk, messagebox

from utilidades.archivos import leer_registros, guardar_registros
from utilidades.base_crud import BaseCRUD
from utilidades.base_pantalla import BasePantalla

ARCHIVO = "datos/proveedores.txt"

def leer_proveedores():
    return leer_registros(ARCHIVO)

def guardar_proveedores(proveedores):
    guardar_registros(ARCHIVO, proveedores)

def abrir_proveedores():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Proveedores")
    ventana.geometry("1050x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    # ---------------- VARIABLES ----------------

    identificador = tk.StringVar()
    razon_social = tk.StringVar()
    cuit = tk.StringVar()
    direccion = tk.StringVar()
    telefono = tk.StringVar()
    email = tk.StringVar()
    estado = tk.StringVar(value="ACTIVO")

    # ---------------- UI BASE ----------------

    ui = BasePantalla(
        ventana,
        "GESTIÓN DE PROVEEDORES",
        ancho_tabla=560
    )

    ui.crear_titulo()
    ui.crear_contenedor_tabla()

    form = ui.crear_contenedor_form()

    tabla = ui.crear_tabla(
        ["id", "razon_social", "cuit", "direccion", "telefono","email", "estado"]
    )

    # -------------- FUNCIONES -------------

    def cargar_tabla(datos=None):
        ui.limpiar_tabla()

        if datos is None:
            datos = leer_proveedores()
        
        for proveedor in datos:
            tabla.insert("", "end", values=proveedor)

    def limpiar_campos():
        identificador.set("")
        razon_social.set("")
        cuit.set("")
        direccion.set("")
        telefono.set("")
        email.set("")
        estado.set("ACTIVO")

    def validar_campos():
        if not crud.validar_requerido(identificador.get(), "Identificador"):
            return False

        if not crud.validar_numerico(identificador.get(), "Identificador"):
            return False

        if not crud.validar_requerido(razon_social.get(), "Razón Social"):
            return False

        if not crud.validar_requerido(cuit.get(), "CUIT"):
            return False

        if not crud.validar_numerico(cuit.get(), "CUIT"):
            return False

        if not crud.validar_requerido(direccion.get(), "Dirección"):
            return False

        if not crud.validar_requerido(telefono.get(), "Telefono"):
            return False

        if not crud.validar_requerido(email.get(), "Email"):
            return False

        return True

    def seleccionar(event):
        seleccion = tabla.focus()

        if seleccion:
            valores = tabla.item(seleccion, "values")

            identificador.set(valores[0])
            razon_social.set(valores[1])
            cuit.set(valores[2])
            direccion.set(valores[3])
            telefono.set(valores[4])
            email.set(valores[5])
            estado.set(valores[6])
    
    # ---------------- CRUD --------------

    crud = BaseCRUD(
        leer_proveedores,
        guardar_proveedores,
        cargar_tabla,
        limpiar_campos
    )

    def alta():
        if not validar_campos():
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
            messagebox.showinfo("Baja", "Proveedor dado de baja correctamente.")
        else:
            messagebox.showerror("Error", "Proveedor no encontrado.")

    def modificar():
        if not validar_campos():
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

        ok = crud.modificar(identificador.get(), nuevo)

        if ok:
            messagebox.showinfo("Modificación", "Proveedor modificado correctamente.")
        else:
            messagebox.showerror("Error", "Proveedor no encontrado.")

    # ----------- FORMULARIO ----------------------

    tk.Label(
        form,
        text="Datos del proveedor",
        font=("Arial", 14, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=identificador, width=30).grid(row=1, column=1, pady=5)

    tk.Label(form, text="Razón Social:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=razon_social, width=30).grid(row=2, column=1, pady=5)

    tk.Label(form, text="CUIT:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=cuit, width=30).grid(row=3, column=1, pady=5)

    tk.Label(form, text="Dirección:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=direccion, width=30).grid(row=4, column=1, pady=5)

    tk.Label(form, text="Teléfono:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=telefono, width=30).grid(row=5, column=1, pady=5)

    tk.Label(form, text="Email:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
    tk.Entry(form, textvariable=email, width=30).grid(row=6, column=1, pady=5)

    tk.Label(form, text="Estado:", bg="white").grid(row=7, column=0, sticky="w", pady=5)

    ttk.Combobox(
        form,
        textvariable=estado,
        values=["ACTIVO", "BAJA"],
        state="readonly",
        width=27
    ).grid(row=7, column=1, pady=5)

    # ---------------- BOTONES ---------------- #

    tk.Button(form, text="Alta", bg="#16A34A", fg="white", command=alta).grid(row=8, column=0, pady=10)
    tk.Button(form, text="Modificar", bg="#2563EB", fg="white", command=modificar).grid(row=8, column=1, pady=10)
    tk.Button(form, text="Baja", bg="#DC2626", fg="white", command=baja).grid(row=9, column=0)
    tk.Button(form, text="Limpiar", bg="#6B7280", fg="white", command=limpiar_campos).grid(row=9, column=1)

    # ----------- TABLA --------------------

    tabla.bind("<<TreeviewSelect>>", seleccionar)
    
    tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white",
        command=ventana.destroy).place(x=900, y=510)

    cargar_tabla()