import streamlit as st
import pandas as pd

from services.producto_service import ProductoService
service = ProductoService()

# -----------------------------------------------

st.title("📦 Gestión de Productos")
st.divider()

productos = service.obtener_todos()
opciones = {}

if productos:
    opciones = {
        f"{p[0]} - {p[1]} {p[2]}": p
        for p in productos
    }

seleccionado = st.selectbox(
    "Seleccionar producto",
    ["Nuevo producto"] + list(opciones.keys())
)

if seleccionado != "Nuevo producto":
    producto = opciones[seleccionado]

    id_default = producto[0]
    descripcion_default = producto[1]
    categoria_default = producto[2]
    precio_default = str(producto[3])
    talle_default = producto[4]
    color_default = producto[5]
    estado_default = producto[6]

else:
    id_default = ""
    descripcion_default = ""
    categoria_default = ""
    precio_default = ""
    talle_default = "M"
    color_default = "NEGRO"
    estado_default = "ACTIVO"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    identificador = st.text_input("ID", value=id_default)
    descripcion = st.text_input("Descripción", value=descripcion_default)
    categoria = st.text_input("Categoria", value=categoria_default)
    precio = st.text_input("Precio", value=precio_default)
    talle = st.selectbox("Talle",  ["XS", "S", "M", "L", "XL", "XXL"],  index=["XS", "S", "M", "L", "XL", "XXL"].index(talle_default))
    color = st.selectbox("Color", ["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"], index=["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"].index(color_default))
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_default == "ACTIVO" else 1)

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕"):
            ok, mensaje = service.alta(identificador, descripcion, categoria, precio, talle, color, estado)
            
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with col_btn2:
        if st.button("✏️"):
            ok, mensaje = service.modificar(identificador, descripcion, categoria, precio, talle, color, estado)
            
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
    st.subheader("📋 Productos registrados")
    
    if productos:
        columnas = ["ID", "Descripción", "Categoria", "Precio", "Talle", "Color", "Estado"]

        df = pd.DataFrame(productos, columns=columnas)
        st.dataframe(df, use_container_width=True)
    
    else:
        st.info("No hay productos registrados")