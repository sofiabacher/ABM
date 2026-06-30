import streamlit as st
import pandas as pd

from io import BytesIO
from services.cliente_service import ClienteService

service = ClienteService()

# ------------------- DATOS -----------------

st.title("👥 Gestión de Clientes")
st.divider()

clientes = service.obtener_todos()
opciones = {}

if clientes:
    opciones = {
        f"{c.id_cliente} - {c.nombre} - {c.apellido}": c
        for c in clientes
    }

seleccionado = st.selectbox(
    "Seleccionar cliente",
    ["Nuevo cliente"] + list(opciones.keys())
)

if seleccionado != "Nuevo cliente":
    cliente = opciones[seleccionado]
    nombre_def = cliente.nombre
    apellido_def = cliente.apellido
    dni_def = cliente.dni
    telefono_def = cliente.telefono
    direccion_def = cliente.direccion
    email_def = cliente.email or ""
    estado_def = cliente.estado

else:
    cliente = None
    nombre_def = ""
    apellido_def = ""
    dni_def = ""
    telefono_def = ""
    direccion_def = ""
    email_def = ""
    estado_def = True

# ---------------- FORMULARIO -----------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    nombre = st.text_input("Nombre", value=nombre_def)
    apellido = st.text_input("Apellido", value=apellido_def)
    dni = st.text_input("DNI", value=dni_def)
    telefono = st.text_input("Teléfono", value=telefono_def)
    direccion = st.text_input("Dirección", value=direccion_def)
    email = st.text_input("Email", value=email_def)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_def else 1)

    estado_bool = estado == "ACTIVO"

    col1_btn1, col_btn2, col_btn3 = st.column(3)

    with col1_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(nombre, apellido, dni, telefono, direccion, email or None, estado_bool)
            st.success(mensaje) if ok else st.error(mensaje)
            if ok:
                st.rerun()
    
    with col_btn2:
        if st.button("✏️ Modificar"):
            if cliente is None:
                st.error("Seleccione un cliente para modificar")
            else:
                ok, mensaje = service.modificar(cliente.id_cliente, nombre, apellido, dni, telefono, direccion, email or None, estado_bool)
                st.success(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

    with col_btn3:
        if st.button("🗑️ Baja"):
            if cliente is None:
                st.error("Seleccione un cliente para dar de baja")
            else:
                ok, mensjae = service.baja(cliente.id_cliente)
                st.warning(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

# ------------- TABLA + BUSCAR CLIENTES -----------------

with col2:
    st.subheader("🔎 Buscar cliente")
    texto_busqueda = st.text_input("Buscar por nombre, apellido o DNI")
    
    lista = clientes
    if texto_busqueda:
        texto = texto_busqueda.lower()
        lista = [
            c for c in clientes
            if texto in c.nombre.lower()
            or texto in c.apellido.lower()
            or texto in c.dni.lower()
        ]

    st.subheader("📋 Clientes registrados")

    if lista:
        df = pd.DataFrame([{
            "ID": c.id_cliente,
            "Nombre": c.nombre,
            "Apellido": c.apellido,
            "DNI": c.dni,
            "Teléfono": c.telefono,
            "Dirección": c.direccion,
            "Email": c.email,
            "Estado": "ACTIVO" if c.estado else "BAJA"
        } for c in lista])

        st.dataframe(df, use_container_width=True)

        excel = BytesIO()
        with pd.ExcelWriter(excel, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Clientes")
        
        st.download_button(
            "📥 Descargar",
            data=excel.getvalue(),
            file_name="clientes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("No hay clientes registrados")