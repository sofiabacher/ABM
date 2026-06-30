import streamlit as st
import plotly.express as px
import pandas as pd

from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from services.proveedor_service import ProveedorService
from services.factura_service import FacturaService

st.set_page_config(
    page_title="ABM Indumentaria",
    page_icon="👕",
    layout="wide"
)

# ---------------- SERVICES -------------------------------

cliente_service = ClienteService()
producto_service = ProductoService()
proveedor_service = ProveedorService()
factura_service = FacturaService()

clientes = cliente_service.obtener_todos()
productos = producto_service.obtener_todos()
proveedores = proveedor_service.obtener_todos()
facturas = factura_service.obtener_facturas()

# ---------------- METRICAS -------------------------------

cant_clientes = len(clientes)
cant_productos = len(productos)
cant_proveedores = len(proveedores)
cant_facturas = len(facturas)

clientes_activos = sum(1 for c in clientes if c.estado)
clientes_baja = sum(1 for c in clientes if not c.estado)
productos_activos = sum(1 for p in productos if p.estado)
productos_baja = sum(1 for p in productos if not p.estado)
proveedores_activos = sum(1 for p in proveedores if p.estado)
proveedores_baja = sum(1 for p in proveedores if not p.estado)

# facturas devuelven tuplas crudas del JOIN (no pasan por from_row de Factura)
facturas_emitidas = sum(1 for f in facturas if f[7] == "EMITIDA")
facturas_anuladas = sum(1 for f in facturas if f[7] == "ANULADA")

# ---------------- UI -------------------------------

st.title("👕 Sistema de Gestión de Indumentaria")
st.write("Bienvenido al sistema de gestión empresarial.")
st.divider()

st.subheader("📊 Resumen general")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Clientes",    cant_clientes)
with col2:
    st.metric("📦 Productos",   cant_productos)
with col3:
    st.metric("🏢 Proveedores", cant_proveedores)
with col4:
    st.metric("🧾 Facturas",    cant_facturas)

col5, col6 = st.columns(2)

with col5:
    st.metric("✅ Facturas emitidas",  facturas_emitidas)
with col6:
    st.metric("🚫 Facturas anuladas", facturas_anuladas)

st.divider()

st.subheader("🧭 Módulos disponibles")

col7, col8, col9, col10 = st.columns(4)

with col7:
    st.info("👥 Clientes")
with col8:
    st.info("📦 Productos")
with col9:
    st.info("🏢 Proveedores")
with col10:
    st.info("🧾 Facturación")

st.divider()

st.subheader("📈 Estadísticas")

col11, col12, col13 = st.columns(3)

with col11:
    datos = pd.DataFrame({
        "Estado":   ["ACTIVO", "BAJA"],
        "Cantidad": [clientes_activos, clientes_baja],
    })

    fig = px.pie(datos, names="Estado", values="Cantidad", title="Clientes")
    st.plotly_chart(fig, use_container_width=True)

with col12:
    datos = pd.DataFrame({
        "Estado":   ["ACTIVO", "BAJA"],
        "Cantidad": [productos_activos, productos_baja],
    })

    fig = px.pie(datos, names="Estado", values="Cantidad", title="Productos")
    st.plotly_chart(fig, use_container_width=True)

with col13:
    datos = pd.DataFrame({
        "Estado":   ["ACTIVO", "BAJA"],
        "Cantidad": [proveedores_activos, proveedores_baja],
    })

    fig = px.pie(datos, names="Estado", values="Cantidad", title="Proveedores")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ALERTAS DE STOCK CRÍTICO -------------------------------

criticos = [p for p in productos if p.necesita_reposicion and p.estado]

if criticos:
    st.divider()
    st.subheader("⚠️ Stock crítico")
    st.warning(f"{len(criticos)} producto(s) con stock igual o por debajo del mínimo.")

    df_criticos = pd.DataFrame([{
        "Código": p.codigo,
        "Producto": p.nombre,
        "Stock actual": p.stock_actual,
        "Stock mínimo": p.stock_minimo,
    } for p in criticos])

    st.dataframe(df_criticos, use_container_width=True)
