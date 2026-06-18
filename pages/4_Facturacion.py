import streamlit as st
import pandas as pd

from services.factura_service import FacturaService
service = FacturaService()

#------------------------------------------

st.title("🧾 Facturación")
st.divider()

clientes = service.obtener_clientes_activos()
productos = service.obtener_productos_activos()
facturas = service.obtener_facturas()

if "items_factura" not in st.session_state:
    st.session_state.items_factura = []

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Datos de la factura")

    cliente = st.selectbox("Cliente", clientes)
    tipo_factura = st.selectbox("Tipo factura", ["A", "B", "C"])
    estado_pago = st.selectbox("Estado de pago", ["PENDIENTE", "PAGADO"])
    producto = st.selectbox("Producto", list(productos.keys()))
    cantidad = st.number_input("Cantidad", min_value=1, value=1)

    if st.button("➕ Agregar producto"):
        precio = productos[producto]
        subtotal = precio * cantidad

        item = {
            "producto": producto,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal
        }

        st.session_state.items_factura.append(item)
        st.rerun()
    
    if st.button("🧾 Generar factura"):
        if len(st.session_state.items_factura) == 0:
            st.error("Debe agregar productos")

        else:
            ok, mensaje = service.generar_factura(cliente, tipo_factura, estado_pago, st.session_state.items_factura)
            
            if ok:
                st.success(mensaje)
                st.session_state.items_factura = []
                st.rerun()
            else:
                st.error(mensaje)

with col2:
    st.subheader("Detalle de la factura")
    
    items = st.session_state.items_factura

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df, use_container_width=True)

        total = sum(item["subtotal"] for item in items)
        st.metric("TOTAL", f"${total:.2f}")
    
    else:
        st.info("No hay productos agregados")

st.divider()
st.subheader("📋 Historial de facturas")

if facturas:
    opciones = {
        f[0]: f
        for f in facturas
    }

    seleccionada = st.selectbox(
        "Seleccionar factura",
        options=opciones.keys()
    )

    factura = opciones[seleccionada]

    st.write("Número:", factura[0])
    st.write("Tipo:", factura[1])
    st.write("Fecha:", factura[2])
    st.write("Total:", factura[3])
    st.write("Estado:", factura[4])
    st.write("Cliente:", factura[5])

    detalle = service.obtener_detalle(seleccionada)

    if detalle:
        columnas = ["Producto", "Cantidad", "Precio", "Subtotal"]
        
        df = pd.DataFrame(detalle, columns=columnas)
        st.dataframe(df, use_container_width=True)

        contenido = ""
        contenido += f"Factura: {factura[0]}\n"
        contenido += f"Fecha: {factura[2]}\n"
        contenido += f"Cliente: {factura[5]}\n"
        contenido += f"Estado: {factura[4]}\n"
        contenido += "\nDETALLE\n"

        for item in detalle:
            contenido += (
                f"{item[0]} |"
                f"{item[1]} |"
                f"${item[2]} |"
                f"${item[3]} |"
            )
        
        contenido += f"\nTOTAL: ${factura[3]}"

        st.download_button(
            "📄 Descargar factura",
            data=contenido,
            file_name=f"factura_{factura[0]}.txt"
        )