import streamlit as st
import pandas as pd

from io import BytesIO
from services.producto_service import ProductoService
from services.categoria_service import CategoriaService

service = ProductoService()
categoria_service = CategoriaService()

# ---------------- DATOS -------------------------------

st.title("📦 Gestión de Productos")
st.divider()

productos = service.obtener_todos()
categorias = categoria_service.obtener_todos

# Mapa id -> nombre para el selectbox
cat_opciones = {c.id_categoria: c.nombre for c in categorias}
cat_nombres = list(cat_opciones.values())
cat_ids = list(cat_opciones.keys())

opciones = {}
if productos:
    opciones = {
        f"{p.id_producto} - {p.codigo} | {p.nombre}": p
        for p in productos
    }

seleccionado = st.selectbox(
    "Seleccionar producto",
    ["Nuevo producto"] + list(opciones.keys())
)

if seleccionado != "Nuevo producto":
    producto = opciones[seleccionado]
    codigo_def = producto.codigo
    nombre_def = producto.nombre
    descripcion_def = producto.descripcion or ""
    precio_c_def = str(producto.precio_compra)
    precio_v_def = str(producto.precio_venta)
    stock_min_def = producto.stock_minimo
    stock_act_def = producto.stock_actual     # solo lectura
    talle_def = producto.talle or "M"
    color_def = producto.color or "NEGRO"
    estado_def = producto.estado
    cat_idx = cat_ids.index(producto.id_categoria) if producto.id_categoria in cat_ids else 0
else:
    producto = None
    codigo_def = ""
    nombre_def = ""
    descripcion_def = ""
    precio_c_def = ""
    precio_v_def = ""
    stock_min_def = 0
    stock_act_def = None
    talle_def = "M"
    color_def = "NEGRO"
    estado_def = True
    cat_idx = 0

# ------------- FORMULARIO ------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    codigo = st.text_input("Código", value=codigo_def)
    nombre = st.text_input("Nombre", value=nombre_def)
    descripcion = st.text_input("Descripción", value=descripcion_def)
    cat_nombre = st.selectbox("Categoría", cat_nombres, index=cat_idx)
    id_categoria= cat_ids[cat_nombres.index(cat_nombre)] if cat_nombres else None

    precio_compra = st.text_input("Precio compra", value=precio_c_def)
    precio_venta = st.text_input("Precio venta", value=precio_v_def)

    talles = ["XS", "S", "M", "L", "XL", "XXL"]
    colores = ["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"]

    talle = st.selectbox("Talle", talles, index=talles.index(talle_def)  if talle_def in talles  else 2)
    color  = st.selectbox("Color",  colores, index=colores.index(color_def) if color_def in colores else 1)
    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_def else 1)

    stock_minimo = st.number_input("Stock mínimo", min_value=0, value=int(stock_min_def))

    if producto is not None:
        st.info(f"📦 Stock actual: **{stock_act_def}** unidades (no editable manualmente)")
    
    estado_bool = estado == "ACTIVO"

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(
                codigo, nombre, precio_compra, precio_venta, id_categoria,
                descripcion or None, talle, color, 0, stock_minimo, estado_bool
            )

            st.success(mensaje) if ok else st.error(mensaje)
            if ok:
                st.rerun()
        
    with col_btn2:
        if st.button("✏️ Modificar"):
            if producto is None:
                st.error("Seleccione un producto para modificar")
                
            else:
                ok, mensaje = service.modificar(
                    producto.id_producto, codigo, nombre,
                    precio_compra, precio_venta, id_categoria,
                    descripcion or None, talle, color, stock_minimo, estado_bool
                )

                st.success(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

    with col_btn3:
        if st.button("🗑️ Baja"):
            if producto is None:
                st.error("Seleccione un producto para dar de baja")
            
            else:
                ok, mensaje = service.baja(producto.id_producto)
                st.warning(mensaje) if ok else st.error(mensaje)
                if ok:
                    st.rerun()

# ------------- TABLA + BUSCAR CLIENTES -----------------

with col2:
    st.subheader("🔎 Buscar producto")
    texto_busqueda = st.text_input("Buscar por código, nombre o descripción")

    lista = productos
    if texto_busqueda:
        texto = texto_busqueda.lower()
        lista = [
            p for p in productos
            if texto in p.codigo.lower()
            or texto in p.nombre.lower()
            or texto in (p.descripcion or "").lower()
        ]

    st.subheader("📋 Productos registrados")

    if lista:
        df = pd.DataFrame([{
            "ID": p.id_producto,
            "Código": p.codigo,
            "Nombre": p.nombre,
            "Categoría": cat_opciones.get(p.id_categoria, "—"),
            "Precio compra": p.precio_compra,
            "Precio venta": p.precio_venta,
            "Talle": p.talle,
            "Color": p.color,
            "Stock actual": p.stock_actual,
            "Stock mínimo": p.stock_minimo,
            "⚠️ Reponer": "Sí" if p.necesita_reposicion else "No",
            "Estado": "ACTIVO" if p.estado else "BAJA",
        } for p in lista])

        st.dataframe(df, use_container_width=True)

        excel = BytesIO()
        with pd.ExcelWriter(excel, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Productos")

        st.download_button(
            "📥 Descargar",
            data=excel.getvalue(),
            file_name="productos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("No hay productos registrados")