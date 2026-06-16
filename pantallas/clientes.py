import tkinter as tk
from tkinter import ttk, messagebox

from services.cliente_service import ClienteService
from utilidades.base_pantalla import BasePantalla

def abrir_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("950x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#f4f6fa")

    # ---------------- VARIABLES ---------------

    identificador = tk.StringVar()
    nombre = tk.StringVar()
    apellido = tk.StringVar()
    dni = tk.StringVar()
    direccion = tk.StringVar()
    estado = tk.StringVar(value="ACTIVO")

    service = ClienteService()

    # ---------------- UI BASE ---------------

    ui = BasePantalla(
        ventana, 
        "GESTIÓN DE CLIENTES", 
        ancho_tabla=470
    )

    ui.crear_titulo()
    ui.crear_contenedor_tabla()

    form = ui.crear_contenedor_form()

    tabla = ui.crear_tabla(
        ["id", "nombre", "apellido", "dni", "direccion", "estado"]
    )

    # -------------- FUNCIONES -------------

    def cargar_tabla():
        ui.limpiar_tabla()

        clientes = service.obtener_todos()

        for cliente in clientes:
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
            valores = tabla.item(seleccion, "values")
            
            identificador.set(valores[0])
            nombre.set(valores[1])
            apellido.set(valores[2])
            dni.set(valores[3])
            direccion.set(valores[4])
            estado.set(valores[5])

    # ---------------- CRUD --------------

    def alta():
        valido, mensaje = service.validar_campos(
            identificador.get(),
            nombre.get(),
            apellido.get(),
            dni.get(),
            direccion.get()
        )

        if not valido:
            messagebox.showerror("Error", mensaje)
            return
        
        ok, mensaje = service.alta(
            identificador.get(),
            nombre.get().strip(),
            apellido.get().strip(),
            dni.get(),
            direccion.get().strip(),
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
            messagebox.showerror("Error", "Debe seleccionar un cliente")
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
            nombre.get(),
            apellido.get(),
            dni.get(),
            direccion.get()
        )

        if not valido:
            messagebox.showerror("Error", mensaje)
            return
        
        ok, mensaje = service.alta(
            identificador.get(),
            nombre.get().strip(),
            apellido.get().strip(),
            dni.get(),
            direccion.get().strip(),
            estado.get()
        )
        
        if ok:
            messagebox.showinfo("OK", mensaje)
            cargar_tabla()

        else:
            messagebox.showerror("Error", mensaje)

    # ----------- FORMULARIO ----------------------

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

    # ----------- TABLA --------------------

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white",
        command=ventana.destroy).place(x=800, y=510)
    
    cargar_tabla()