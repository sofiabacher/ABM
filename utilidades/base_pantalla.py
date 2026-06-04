import tkinter as tk
from tkinter import ttk

class BasePantalla:
    def __init__(self, ventana, titulo, ancho_tabla=500):
        self.ventana = ventana
        self.titulo = titulo
        self.ancho_tabla = ancho_tabla

        self.tabla = None
        self.form_frame = None
        self.tabla_frame = None

    def crear_titulo(self):
        tk.Label(
            self.ventana,
            text=self.titulo,
            font=("Arial", 22, "bold"),
            bg="#f4f6fa",
            fg="#172033"
        ).pack(pady=15)

    def crear_contenedor_form(self, width=390, height=450):
        self.form_frame = tk.Frame(self.ventana, bg="white", padx=20, pady=20)
        self.form_frame.place(x=30, y=80, width=width, height=height)
        return self.form_frame
    
    def crear_contenedor_tabla(self, x=450, y=80, height=420):
        self.tabla_frame = tk.Frame(self.ventana, bg="white")
        self.tabla_frame.place(x=x, y=y, width=self.ancho_tabla, height=height)
        return self.tabla_frame
    
    def crear_tabla(self, columnas):
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            columns=columnas,
            show="headings"
        )

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            self.tabla_frame,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

        return self.tabla
    
    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def cargar_datos_tabla(self, datos):
        self.limpiar_tabla()
        for d in datos:
            self.tabla.insert("", "end", values=d)

