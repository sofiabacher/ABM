from tkinter import messagebox

class BaseCRUD:
    def __init__(self, leer, guardar, insertar, limpiar):
        self.leer = leer
        self.guardar = guardar
        self.insertar = insertar
        self.limpiar = limpiar

    # ------------ VALIDACIONES ----------------

    def validar_id(self, id_value):
        if id_value == "":
            messagebox.showwarning("Atención", "Debe ingresar un identificador.")
            return False

        if not id_value.isdigit():
            messagebox.showwarning("Atención", "El identificador debe ser numérico.")
            return False

        return True

    def validar_requerido(self, valor, nombre_campo):
        if valor.strip() == "":
            messagebox.showwarning("Atención", f"Debe completar {nombre_campo}.")
            return False

        return True

    def validar_numerico(self, valor, nombre_campo):
        if valor == "":
            messagebox.showwarning("Atención", f"Debe completar {nombre_campo}.")
            return False

        try:
            float(valor)
        except ValueError:
            messagebox.showwarning( "Atención", f"{nombre_campo} debe ser numérico.")
            return False

        return True
    
    # ----------------- CRUD --------------------

    def alta(self, nuevo_registro, campo_id=None):
        datos = self.leer()

        if campo_id is not None:
            for d in datos:
                if d[0] == campo_id:
                    return "ERROR_DUPLICADO"
        
        datos.append(nuevo_registro)
        self.guardar(datos)
        self.insertar(datos)
        self.limpiar()

        return "OK"
    
    def baja(self, id_value):
        datos = self.leer()
        encontrado = False

        for d in datos:
            if d[0] == id_value:
                d[-1] = "BAJA"  # se asume que el último campo de la tabla es "estado"
                encontrado = True
        
        self.guardar(datos)
        self.insertar(datos)

        return encontrado
    
    def modificar(self, id_value, nuevos_datos):
        datos = self.leer()
        encontrado = False

        for i in range(len(datos)):
            if datos[i][0] == id_value:
                datos[i] = nuevos_datos
                encontrado = True
        
        self.guardar(datos)
        self.insertar(datos)

        return encontrado