import streamlit as st
import pandas as pd

from services.cliente_service import ClienteService
service = ClienteService()

# -----------------------------------------------

st.title("👥 Gestión de Clientes")
st.divider()

clientes = service.obtener_todos()
opciones = {}

if clientes:
    opciones = {
        f"{c[0]} - {c[1]} {c[2]}": c
        for c in clientes
    }

seleccionado = st.selectbox(
    "Seleccionar cliente",
    ["Nuevo cliente"] + list(opciones.keys())
)

if seleccionado != "Nuevo cliente":
    cliente = opciones[seleccionado]

    id_default = cliente[0]
    nombre_default = cliente[1]
    apellido_default = cliente[2]
    dni_default = cliente[3]
    direccion_default = cliente[4]
    estado_default = cliente[5]

else:
    id_default = ""
    nombre_default = ""
    apellido_default = ""
    dni_default = ""
    direccion_default = ""
    estado_default = "ACTIVO"

col1, col2 = st.columns([1, 2])    # FORMULARIO

with col1:
    st.subheader("Formulario")

    identificador = st.text_input("ID", value=id_default)
    nombre = st.text_input("Nombre", value=nombre_default)
    apellido = st.text_input("Apellido", value=apellido_default)
    dni = st.text_input("DNI", value=dni_default)
    direccion = st.text_input("Dirección", value=direccion_default)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_default == "ACTIVO" else 1)

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕"):
            ok, mensaje = service.alta(identificador, nombre, apellido, dni, direccion, estado)
            
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with col_btn2:
        if st.button("✏️"):
            ok, mensaje = service.modificar(identificador, nombre, apellido, dni, direccion, estado)
            
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with col_btn3:
        if st.button("🗑️"):
            ok, mensaje = service.baja(identificador)
            
            if ok:
                st.warning(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

with col2:
    st.subheader("📋 Clientes registrados")
    
    if clientes:
        columnas = ["ID", "Nombre", "Apellido", "DNI", "Dirección", "Estado"]

        df = pd.DataFrame(clientes, columns=columnas)
        st.dataframe(df, use_container_width=True)
    
    else:
        st.info("No hay clientes registrados")