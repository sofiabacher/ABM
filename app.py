import streamlit as st

from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from services.proveedor_service import ProveedorService

cliente_service = ClienteService()
producto_service = ProductoService()
proveedor_service = ProveedorService()

cant_clientes = len(cliente_service.obtener_todos())
cant_productos = len(producto_service.obtener_todos())
cant_proveedores = len(proveedor_service.obtener_todos())

# --------------------------------------------

st.set_page_config(
    page_title="ABM Indumentaria",
    page_icon="👕",
    layout="wide"
)

st.title("👕 Sistema de Gestión de Indumentaria")

st.markdown("""
### Bienvenido 
Desde el menú lateral podrás administrar toda la información del negocio.
""")

st.divider()
st.subheader("📊 Resumen general")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="👥 Clientes",
        value=cant_clientes
    )

with col2:
    st.metric(
        label="📦 Productos",
        value=cant_productos
    )

with col3:
    st.metric(
        label="🏢 Proveedores",
        value=cant_proveedores
    )

st.divider()

st.subheader("🧭 Módulos disponibles")

col4, col5, col6, col7 = st.columns(4)

with col4:
    st.info("👥 Clientes")

with col5:
    st.info("📦 Productos")

with col6:
    st.info("🏢 Proveedores")

with col7:
    st.info("🧾 Facturación")