import os

def crear_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        open(nombre_archivo, "w").close()


def leer_registros(nombre_archivo):
    crear_archivo(nombre_archivo)
    registros = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")

            if len(datos) > 0:
                registros.append(datos)
    
    return registros


def guardar_registros(nombre_archivo, registros):
    with open(nombre_archivo, "w") as archivo:
        for registro in registros:
            archivo.write("|".join(registro) + "\n")

