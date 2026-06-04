class BaseCRUD:
    def __init__(self, leer, guardar, insertar, limpiar):
        self.leer = leer
        self.guardar = guardar
        self.insertar = insertar
        self.limpiar = limpiar

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