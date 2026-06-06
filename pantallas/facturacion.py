import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from utilidades.archivos import leer_registros
from utilidades.base_pantalla import BasePantalla

# ----------- ARCHIVOS -----------------------

FACTURAS = "datos/facturas.txt"
CLIENTES = "datos/clientes.txt"
PRODUCTOS = "datos/productos.txt"

def leer_clientes():
    return leer_registros(CLIENTES)

def leer_productos():
    return leer_registros(PRODUCTOS)

def abrir_facturacion():
    ventana = tk.Toplevel()
    ventana.title("Facturación")
    ventana.geometry("1100x600")
    ventana.resizable(False, False)
    ventana.config(bg="#f4f6fa")

    # --------- VARIABLES -----------------

    cliente = tk.StringVar()
    producto = tk.StringVar()
    cantidad = tk.StringVar(value=1)
    tipo_factura = tk.StringVar(value="A")
    estado_pago = tk.StringVar(value="PENDIENTE")

    items_factura = []

    # --------- UI BASE ----------------

    ui = BasePantalla(
        ventana,
        "FACTURACIÓN",
        ancho_tabla=650
    )

    ui.crear_titulo()

    form = ui.crear_contenedor_form(width=420, height=520)

    frame_factura = tk.Frame(ventana, bg="white")
    frame_factura.place(x=470, y=80, width=680, height=520)

    # --------- DATOS -----------------

    clientes = [
        f"{c[0]} - {c[1]} {c[2]}"
        for c in leer_clientes()
        if c[5] == "ACTIVO"
    ]

    productos = {
        f"{p[0]} - {p[1]}": float(p[3])
        for p in leer_productos()
        if p[6] == "ACTIVO"
    }

    # ---------------- FORM -------------
    
    tk.Label(form, text="Datos de la factura", bg="white", 
        font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form, text="Cliente:", bg="white").grid(row=1, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=cliente,
        values=clientes,
        state="readonly",
        width=30
    ).grid(row=1, column=1)

    tk.Label(form, text="Tipo Factura:", bg="white").grid(row=2, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=tipo_factura,
        values=["A", "B", "C"],
        width=30,
        state="readonly"
    ).grid(row=2, column=1)

    tk.Label(form, text="Estado pago:", bg="white").grid(row=3, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=estado_pago,
        values=["PENDIENTE", "PAGADO"],
        width=30,
        state="readonly"
    ).grid(row=3, column=1)

    tk.Label(form, text="Producto:", bg="white").grid(row=4, column=0, sticky="w")

    ttk.Combobox(
        form,
        textvariable=producto,
        values=list(productos.keys()),
        state="readonly",
        width=30
    ).grid(row=4, column=1)

    tk.Label(form, text="Cantidad:", bg="white").grid(row=5, column=0, sticky="w")
    tk.Entry(form, textvariable=cantidad, width=33).grid(row=5, column=1)

    # --------------- TABLA FACTURA -------------

    tabla = ttk.Treeview(
        frame_factura,
        columns=("producto", "precio", "cantidad", "subtotal"),
        show="headings"
    )

    tabla.heading("producto", text="Producto")
    tabla.heading("precio", text="Precio")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("subtotal", text="Subtotal")

    tabla.column("producto", width=250)
    tabla.column("precio", width=100)
    tabla.column("cantidad", width=100)
    tabla.column("subtotal", width=120)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    total_label = tk.Label(
        frame_factura,
        text="TOTAL: $0",
        font=("Arial", 14, "bold"),
        bg="white"
    )

    total_label.pack(pady=10)

    # ------------ FUNCIONES ---------------

    def actualizar_total():
        total = sum(item["subtotal"] for item in items_factura)
        total_label.config(text=f"TOTAL: ${total:.2f}")

        return total
    
    def agregar_producto():
        if producto.get() == "":
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
        
        try:
            cant = int(cantidad.get())
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        
        precio = productos[producto.get()]
        subtotal = precio * cant

        item = {
            "producto": producto.get(),
            "precio": precio,
            "cantidad": cant,
            "subtotal": subtotal
        }

        items_factura.append(item)

        tabla.insert("", "end", values=(
            item["producto"],
            item["precio"],
            item["cantidad"],
            item["subtotal"]
        ))

        actualizar_total()
    
    def generar_factura():
        if cliente.get() == "":
            messagebox.showwarning("Atención", "Seleccione un cliente")
            return
        
        if len(items_factura) == 0:
            messagebox.showwarning("Atención", "Debe agregar productos")
            return
        
        numero = datetime.now().strftime("%Y%m%d%H%M%S")
        total = actualizar_total()

        with open("datos/facturas.txt", "a", encoding="utf-8") as archivo_facturas:
            archivo_facturas.write(
                f"{numero}|"
                f"{tipo_factura.get()}|"
                f"{datetime.now().strftime('%d/%m/%Y')}|"
                f"{total}|"
                f"{estado_pago.get()}|"
                f"{cliente.get()}\n" 
            )

            with open("datos/detalle_factura.txt", "a", encoding="utf-8") as archivo_detalle:
                for item in items_factura:
                    archivo_detalle.write(
                        f"{numero}|"
                        f"{item['producto']}| "
                        f"{item['cantidad']}|"
                        f"{item['precio']}|"
                        f"{item['subtotal']}\n"
                    )

            messagebox.showinfo("OK", "Factura generada correctamente")
            ventana.destroy()

# --------- BOTONES -----------------

    tk.Button(
        form,
        text="Agregar Producto",
        bg="#2563EB",
        fg="white",
        command=agregar_producto
    ).grid(row=6, column=0, columnspan=2, pady=15)

    tk.Button(
        form,
        text="Generar Factura",
        bg="#16A34A",
        fg="white",
        command=generar_factura
    ).grid(row=7, column=0, columnspan=2, pady=5)

    tk.Button(
        ventana,
        text="Salir",
        width=15,
        bg="#111827",
        fg="white",
        command=ventana.destroy
    ).place(x=920, y=540)