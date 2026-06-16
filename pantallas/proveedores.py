import tkinter as tk
from tkinter import ttk, messagebox

from services.proveedor_service import ProveedorService
from utilidades.base_pantalla import BasePantalla

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

    service = ProveedorService()

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

    def cargar_tabla():
        ui.limpiar_tabla()
        
        proveedores = service.obtener_todos()
        
        for proveedor in proveedores:
            tabla.insert("", "end", values=proveedor)

    def limpiar_campos():
        identificador.set("")
        razon_social.set("")
        cuit.set("")
        direccion.set("")
        telefono.set("")
        email.set("")
        estado.set("ACTIVO")

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

    def alta():
        valido, mensaje = service.validar_campos(
            identificador.get(),
            razon_social.get(),
            cuit.get(),
            direccion.get(),
            telefono.get(),
            email.get()
        )

        if not valido:
            messagebox.showerror("Error", mensaje)
            return
        
        ok, mensaje = service.alta(
            identificador.get(),
            razon_social.get().strip(),
            cuit.get(),
            direccion.get().strip(),
            telefono.get().strip(),
            email.get().strip(),
            estado.get()
        )

        if ok:
            messagebox.showinfo("OK", mensaje)
            cargar_tabla()
            limpiar_campos()

        else:
            messagebox.showerror("Error", mensaje)

    def baja():
        if identificador.get() == "":
            messagebox.showerror("Error", "Debe seleccionar un proveedor")
            return

        ok, mensaje = service.baja(identificador.get())

        if ok:
            messagebox.showinfo("OK", mensaje)
            cargar_tabla()
            limpiar_campos()

        else:
            messagebox.showerror("Error", mensaje)
            
    def modificar():
        valido, mensaje = service.validar_campos(
            identificador.get(),
            razon_social.get(),
            cuit.get(),
            direccion.get(),
            telefono.get(),
            email.get()
        )

        if not valido:
            messagebox.showerror("Error", mensaje)
            return
        
        ok, mensaje = service.alta(
            identificador.get(),
            razon_social.get().strip(),
            cuit.get(),
            direccion.get().strip(),
            telefono.get().strip(),
            email.get().strip(),
            estado.get()
        )

        if ok:
            messagebox.showinfo("OK", mensaje)
            cargar_tabla()
            limpiar_campos()

        else:
            messagebox.showerror("Error", mensaje)

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