import streamlit as st
import pandas as pd

from services.factura_service import FacturaService

service = FacturaService()

# ---------------- DATOS -------------------------------

st.title("🧾 Historila de Facturas")
st.write("Las facturas se generan automáticamente al confirmar una venta desde el módulo **Ventas**.")
st.divider()

facturas  = service.obtener_facturas()

if not facturas:
    st.info("No hay facturas registradas. Registrá una venta para generar la primera.")
    st.stop()

# ------------- TABLA RESUMEN ------------------

df = pd.DataFrame([{
    "N° Factura": f[1],
    "Tipo": f[2],
    "Fecha": f[3],
    "Cliente": f"{f[9]} {f[10]}",
    "Subtotal": f"${f[4]:.2f}",
    "Impuestos": f"${f[5]:.2f}",
    "Total": f"${f[6]:.2f}",
    "Estado": f[7],
} for f in facturas])

st.dataframe(df, use_container_width=True)

# ------------- DETALLE DE LA FACTURA ------------------

st.divider()
st.subheader("🔍 Detalle de una factura")

opciones = {
    f"{f[1]} | {f[9]} {f[10]} | {f[3].strftime('%d/%m/%Y') if hasattr(f[3], 'strftime') else f[3]}": f
    for f in facturas
}

seleccionada_key = st.selectbox("Seleccionar factura", list(opciones.keys()))
factura = opciones[seleccionada_key]

col1, col2 = st.columns(2)

with col1:
    st.write("**N° Factura:**", factura[1])
    st.write("**Tipo:**", factura[2])
    st.write("**Fecha:**", factura[3])
    st.write("**Estado:**", factura[7])

with col2:
    st.write("**Cliente:**", f"{factura[9]} {factura[10]}")
    st.write("**Subtotal:**", f"${factura[4]:.2f}")
    st.write("**Impuestos:**", f"${factura[5]:.2f}")
    st.write("**Total:**", f"${factura[6]:.2f}")

detalle = service.obtener_detalle(factura[8])   # factura[8] = id_venta

if detalle:
    df_det = pd.DataFrame(
        detalle,
        columns=["Producto", "Cantidad", "Precio unitario", "Subtotal"]
    )
    st.dataframe(df_det, use_container_width=True)
    
    fecha_str = (
        factura[3].strftime("%d/%m/%Y %H:%M")
        if hasattr(factura[3], "strftime") else str(factura[3])
    )

    contenido = f"FACTURA {factura[1]}\n"
    contenido += f"{'=' * 40}\n"
    contenido += f"Tipo: {factura[2]}\n"
    contenido += f"Fecha: {fecha_str}\n"
    contenido += f"Cliente: {factura[9]} {factura[10]}\n"
    contenido += f"Estado: {factura[7]}\n\n"
    contenido += "DETALLE\n"
    contenido += f"{'-' * 55}\n"

    for item in detalle:
        contenido += f"{item[0]:<25} | cant: {item[1]:>4} | ${item[2]:>8.2f} | ${item[3]:>10.2f}\n"
    
    contenido += f"{'-' * 55}\n"
    contenido += f"Subtotal: ${factura[4]:.2f}\n"
    contenido += f"Impuestos: ${factura[5]:.2f}\n"
    contenido += f"TOTAL: ${factura[6]:.2f}\n"

    st.download_button(
        "📄 Descargar factura",
        data=contenido,
        file_name=f"factura_{factura[1]}.txt"
    )