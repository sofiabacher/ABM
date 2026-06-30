import streamlit as st
import pandas as pd

from services.categoria_service import CategoriaService

service = CategoriaService()

# ---------------- DATOS -------------------------------

st.title("🗂️ Gestión de Categorías")
st.divider()

categorias = service.obtener_todos()

opciones = {}
if categorias:
    opciones = {
        f"{c.id_categoria} - {c.nombre}": c
        for c in categorias
    }

seleccionado = st.selectbox(
    "Seleccionar categoría",
    ["Nueva categoría"] + list(opciones.keys())
)

if seleccionado != "Nueva categoría":
    categoria = opciones[seleccionado]
    nombre_def = categoria.nombre
    descripcion_def = categoria.descripcion or ""

else:
    categoria = None
    nombre_def = ""
    descripcion_def = ""

# ------------- FORMULARIO CARGAR DATOS ------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    nombre = st.text_input("Nombre", value=nombre_def)
    descripcion = st.text_input("Descripción", value=descripcion_def)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(nombre, descripcion or None)
            st.success(mensaje) if ok else st.error(mensaje)
            
            if ok:
                st.rerun()

    with col_btn2:
        if st.button("✏️ Modificar"):
            if categoria is None:
                st.error("Seleccione una categoría para modificar")
            
            else:
                ok, mensaje = service.modificar(categoria.id_categoria, nombre, descripcion or None)
                st.success(mensaje) if ok else st.error(mensaje)
                
                if ok:
                    st.rerun()

# ------------- TABLA ------------------

with col2:
    st.subheader("📋 Categorías registradas")

    if categorias:
        df = pd.DataFrame([{
            "ID": c.id_categoria,
            "Nombre": c.nombre,
            "Descripción": c.descripcion or "",
        } for c in categorias])

        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("No hay categorías registradas")