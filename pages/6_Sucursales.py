import streamlit as st
import pandas as pd

from services.sucursal_service import SucursalService

service = SucursalService()

# ---------------- DATOS -------------------------------

st.title("🏪 Gestión de Sucursales")
st.divider()

sucursales = service.obtener_todos()

opciones = {}
if sucursales:
    opciones = {
        f"{s.id_sucursal} - {s.nombre}": s
        for s in sucursales
    }

seleccionado = st.selectbox(
    "Seleccionar sucursal",
    ["Nueva sucursal"] + list(opciones.keys())
)

if seleccionado != "Nueva sucursal":
    sucursal = opciones[seleccionado]
    nombre_def = sucursal.nombre
    direccion_def = sucursal.direccion
    ciudad_def = sucursal.ciudad
    provincia_def = sucursal.provincia
    telefono_def = sucursal.telefono
    email_def = sucursal.email
    estado_def = sucursal.estado
else:
    sucursal = None
    nombre_def = ""
    direccion_def = ""
    ciudad_def = ""
    provincia_def = ""
    telefono_def = ""
    email_def = ""
    estado_def = True

# ---------------- FORMULARIO -------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    nombre = st.text_input("Nombre",    value=nombre_def)
    direccion = st.text_input("Dirección", value=direccion_def)
    ciudad = st.text_input("Ciudad",    value=ciudad_def)
    provincia = st.text_input("Provincia", value=provincia_def)
    telefono = st.text_input("Teléfono", value=telefono_def)
    email = st.text_input("Email",    value=email_def)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_def else 1)

    estado_bool = estado == "ACTIVO"

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(nombre, direccion, ciudad, provincia, telefono, email, estado_bool)
            st.success(mensaje) if ok else st.error(mensaje)
            
            if ok:
                st.rerun()

    with col_btn2:
        if st.button("✏️ Modificar"):
            if sucursal is None:
                st.error("Seleccione una sucursal para modificar")
            
            else:
                ok, mensaje = service.modificar(sucursal.id_sucursal, nombre, direccion, ciudad, provincia, telefono, email, estado_bool)
                st.success(mensaje) if ok else st.error(mensaje)
                
                if ok:
                    st.rerun()

    with col_btn3:
        if st.button("🗑️ Baja"):
            if sucursal is None:
                st.error("Seleccione una sucursal para dar de baja")
            
            else:
                ok, mensaje = service.baja(sucursal.id_sucursal)
                st.warning(mensaje) if ok else st.error(mensaje)
                
                if ok:
                    st.rerun()

# ---------------- TABLA -------------------------------

with col2:
    st.subheader("📋 Sucursales registradas")

    if sucursales:
        df = pd.DataFrame([{
            "ID": s.id_sucursal,
            "Nombre": s.nombre,
            "Ciudad": s.ciudad,
            "Provincia": s.provincia,
            "Teléfono": s.telefono,
            "Email": s.email,
            "Estado": "ACTIVO" if s.estado else "BAJA",
        } for s in sucursales])

        st.dataframe(df, use_container_width=True)
    
    else:
        st.info("No hay sucursales registradas")
