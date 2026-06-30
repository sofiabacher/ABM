import streamlit as st
import pandas as pd

from io import BytesIO
from services.proveedor_service import ProveedorService

service = ProveedorService()

# ---------------- DATOS -------------------------------

st.title("🏢 Gestión de Proveedores")
st.divider()

proveedores = service.obtener_todos()

opciones = {}
if proveedores:
    opciones = {
        f"{p.id_proveedor} - {p.razon_social}": p
        for p in proveedores
    }

seleccionado = st.selectbox(
    "Seleccionar proveedor",
    ["Nuevo proveedor"] + list(opciones.keys())
)

if seleccionado != "Nuevo proveedor":
    proveedor = opciones[seleccionado]
    razon_social_def = proveedor.razon_social
    cuit_def = proveedor.cuit
    email_def = proveedor.email
    telefono_def = proveedor.telefono
    provincia_def = proveedor.provincia
    direccion_def = proveedor.direccion
    estado_def = proveedor.estado

else:
    proveedor = None
    razon_social_def = ""
    cuit_def = ""
    email_def = ""
    telefono_def = ""
    provincia_def = ""
    direccion_def = ""
    estado_def = True

# ------------- FORMULARIO ------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    razon_social = st.text_input("Razón Social", value=razon_social_def)
    cuit = st.text_input("CUIT", value=cuit_def)
    email = st.text_input("Email", value=email_def)
    telefono = st.text_input("Teléfono", value=telefono_def)
    provincia = st.text_input("Provincia", value=provincia_def)
    direccion = st.text_input("Dirección", value=direccion_def)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_def else 1)

    estado_bool = estado == "ACTIVO"

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(razon_social, cuit, email, telefono, provincia, direccion, estado_bool)
            st.success(mensaje) if ok else st.error(mensaje)
            if ok:
                st.rerun()
        
    with col_btn2:
        if st.button("✏️ Modificar"):
            if proveedor is None:
                st.error("Seleccione un proveedor para modificar")
                
            else:
                ok, mensaje = service.modificar(
                    proveedor.id_proveedor, razon_social, cuit, email,
                    telefono, provincia, direccion, estado_bool
                )

                st.success(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

    with col_btn3:
        if st.button("🗑️ Baja"):
            if proveedor is None:
                st.error("Seleccione un proveedor para dar de baja")
            
            else:
                ok, mensaje = service.baja(proveedor.id_proveedor)
                st.warning(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

# ------------- TABLA + BUSCAR CLIENTES -----------------

with col2:
    st.subheader("🔎 Buscar proveedor")
    texto_busqueda = st.text_input("Buscar por razón social, CUIT o email")

    lista = proveedores
    if texto_busqueda:
        texto = texto_busqueda.lower()
        lista = [
            p for p in proveedores
            if texto in p.razon_social.lower()
            or texto in p.cuit.lower()
            or texto in p.email.lower()
        ]

    st.subheader("📋 Proveedores registrados")

    if lista:
        df = pd.DataFrame([{
            "ID": p.id_proveedor,
            "Razón Social": p.razon_social,
            "CUIT": p.cuit,
            "Email": p.email,
            "Teléfono": p.telefono,
            "Provincia": p.provincia,
            "Dirección": p.direccion,
            "Estado": "ACTIVO" if p.estado else "BAJA",
        } for p in lista])

        st.dataframe(df, use_container_width=True)

        excel = BytesIO()
        with pd.ExcelWriter(excel, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Proveedores")

        st.download_button(
            "📥 Descargar",
            data=excel.getvalue(),
            file_name="proveedores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("No hay proveedores registrados")