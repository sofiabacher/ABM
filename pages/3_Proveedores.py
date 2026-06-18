import streamlit as st
import pandas as pd

from io import BytesIO

from services.proveedor_service import ProveedorService
service = ProveedorService()

# -----------------------------------------------

st.title("🏢 Gestión de Proveedores")
st.divider()

proveedores = service.obtener_todos()
opciones = {}

if proveedores:
    opciones = {
        f"{p[0]} - {p[1]} {p[2]}": p
        for p in proveedores
    }

seleccionado = st.selectbox(
    "Seleccionar proveedor",
    ["Nuevo proveedor"] + list(opciones.keys())
)

if seleccionado != "Nuevo proveedor":
    proveedor = opciones[seleccionado]

    id_default = proveedor[0]
    razon_social_default = proveedor[1]
    cuit_default = proveedor[2]
    direccion_default = proveedor[3]
    telefono_default = proveedor[4]
    email_default = proveedor[5]
    estado_default = proveedor[6]

else:
    id_default = ""
    razon_social_default = ""
    cuit_default = ""
    direccion_default = ""
    telefono_default = ""
    email_default = ""
    estado_default = "ACTIVO"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    identificador = st.text_input("ID", value=id_default)
    razon_social = st.text_input("Razón Social", value=razon_social_default)
    cuit = st.text_input("CUIT", value=cuit_default)
    direccion = st.text_input("Dirección", value=direccion_default)
    telefono = st.text_input("Teléfono", value=telefono_default)
    email = st.text_input("Email", value=email_default)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_default == "ACTIVO" else 1)

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕"):
            ok, mensaje = service.alta(identificador, razon_social, cuit, direccion, telefono, email, estado)
            
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with col_btn2:
        if st.button("✏️"):
            ok, mensaje = service.modificar(identificador, razon_social, cuit, direccion, telefono, email, estado)
            
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
    st.subheader("🔎 Buscar proveedor")

    texto_busqueda = st.text_input("Buscar por CUIT, teléfono o email")

    if texto_busqueda:
        texto = texto_busqueda.lower()
        proveedores = [
            p for p in proveedores
            if (texto in str(p[1]).lower() or texto in str(p[2]).lower() or texto in str(p[3]).lower())
        ]

    st.subheader("📋 Proveedores registrados")
    
    if proveedores:
        columnas = ["ID", "Razón Social", "CUIT", "Dirección", "Teléfono", "Email", "Estado"]

        df = pd.DataFrame(proveedores, columns=columnas)
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
        st.info("No hay proveedores registrados")