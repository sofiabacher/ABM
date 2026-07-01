import streamlit as st
import pandas as pd

from decimal import Decimal
from services.venta_service import VentaService

service = VentaService()

ID_USUARIO_SESION  = 1
ID_SUCURSAL_SESION = 1

# ---------------- DATOS -------------------------------

st.title("💰 Gestión de Ventas")
st.divider()

clientes = service.obtener_clientes_activos()
productos = service.obtener_productos_activos()
ventas = service.obtener_ventas()

if "items_venta" not in st.session_state:
    st.session_state.items_venta = []

# ---------------- FORMULARIO ------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Nueva venta")

    if not clientes:
        st.warning("No hay clientes activos. Agregue uno antes de registrar una venta.")
        st.stop()

    cliente_sel = st.selectbox("Cliente", clientes)
    tipo_factura = st.selectbox("Tipo de factura", ["A", "B", "C"])
    metodo_pago = st.selectbox("Método de pago", ["EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA"])

    st.markdown("---")
    st.caption("Agregar productos al carrito")

    producto_sel = st.selectbox("Producto", list(productos.keys()))
    prod_data = productos.get(producto_sel, {})
    stock_disp = prod_data.get("stock_actual", 0)

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        max_value=max(stock_disp, 1),
        value=1
    )

    if stock_disp <= 0:
        st.warning("⚠️ Sin stock disponible para este producto")
    else:
        st.caption(f"Stock disponible: {stock_disp} unidades")

    if st.button("➕ Agregar al carrito"):
        if stock_disp < cantidad:
            st.error(f"Stock insuficiente. Disponible: {stock_disp}")
        
        else:
            precio = prod_data["precio"]
            subtotal = precio * cantidad

            # Validar que no supere el stock sumando lo ya agregado al carrito
            ya_en_carrito = sum(
                i["cantidad"]
                for i in st.session_state.items_venta
                if i["id_producto"] == prod_data["id_producto"]
            )

            if ya_en_carrito + cantidad > stock_disp:
                st.error(
                    f"Cantidad total ({ya_en_carrito + cantidad}) "
                    f"supera el stock disponible ({stock_disp})"
                )

            else:
                item = {
                    "id_producto": prod_data["id_producto"],
                    "producto": producto_sel,
                    "precio_unitario": precio,
                    "cantidad": cantidad,
                    "subtotal": subtotal,
                }

                st.session_state.items_venta.append(item)
                st.rerun()

    st.markdown("---")

    if st.button("✅ Confirmar venta", type="primary"):
        if not st.session_state.items_venta:
            st.error("Debe agregar al menos un producto")
        
        else:
            id_cliente = int(cliente_sel.split(" - ")[0])

            ok, mensaje = service.registrar_venta(
                id_cliente=id_cliente,
                id_usuario=ID_USUARIO_SESION,
                id_sucursal=ID_SUCURSAL_SESION,
                tipo_factura=tipo_factura,
                metodo_pago=metodo_pago,
                items=st.session_state.items_venta,
            )

            if ok:
                st.success(mensaje)
                st.session_state.items_venta = []
                st.rerun()

            else:
                st.error(mensaje)

# ---------------- CARRITO ------------------------------

with col2:
    st.subheader("Carrito")

    items = st.session_state.items_venta

    if items:
        df = pd.DataFrame([{
            "Producto": i["producto"],
            "Precio unitario": f"${i['precio_unitario']:.2f}",
            "Cantidad": i["cantidad"],
            "Subtotal": f"${i['subtotal']:.2f}",
        } for i in items])

        st.dataframe(df, use_container_width=True)

        subtotal = sum(i["subtotal"] for i in items)
        iva = (subtotal * Decimal("0.21")).quantize(Decimal("0.01"))

        st.metric("Subtotal", f"${subtotal:.2f}")
        st.metric("IVA (21%)", f"${iva:.2f}")
        st.metric("TOTAL", f"${subtotal + iva:.2f}")

        if st.button("🗑️ Vaciar carrito"):
            st.session_state.items_venta = []
            st.rerun()

    else:
        st.info("El carrito está vacío")

# ---------------- HISTORIAL  ------------------------------

st.divider()
st.subheader("📋 Historial de ventas")

if ventas:
    df_hist = pd.DataFrame([{
        "ID": v[0],
        "Fecha": v[1],
        "Cliente": f"{v[4]} {v[5]}",
        "Método pago": v[2],
        "Total": f"${v[3]:.2f}",
        "Factura": v[6] or "—",
    } for v in ventas])

    st.dataframe(df_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 Detalle de una venta")

    opciones_v = {
        f"#{v[0]} | {v[4]} {v[5]} | {v[1].strftime('%d/%m/%Y') if hasattr(v[1], 'strftime') else v[1]}": v
        for v in ventas
    }

    seleccionada = st.selectbox("Seleccionar venta", list(opciones_v.keys()))
    venta = opciones_v[seleccionada]
    detalle = service.obtener_detalle_venta(venta[0])

    if detalle:
        df_det = pd.DataFrame(
            detalle,
            columns=["Producto", "Cantidad", "Precio unitario", "Subtotal"]
        )

        st.dataframe(df_det, use_container_width=True)

        fecha_str = (
            venta[1].strftime("%d/%m/%Y %H:%M")
            if hasattr(venta[1], "strftime") else str(venta[1])
        )

        contenido  = f"VENTA #{venta[0]}\n"
        contenido += f"{'=' * 40}\n"
        contenido += f"Cliente: {venta[4]} {venta[5]}\n"
        contenido += f"Fecha: {fecha_str}\n"
        contenido += f"Método pago: {venta[2]}\n"
        contenido += f"Factura: {venta[6] or '—'}\n\n"
        contenido += "DETALLE\n"
        contenido += f"{'-' * 55}\n"

        for item in detalle:
            contenido += f"{item[0]:<25} | cant: {item[1]:>4} | ${item[2]:>8.2f} | ${item[3]:>10.2f}\n"
        
        contenido += f"{'-' * 55}\n"
        contenido += f"TOTAL: ${venta[3]:.2f}\n"

        st.download_button(
            "📄 Descargar comprobante",
            data=contenido,
            file_name=f"venta_{venta[0]}.txt"
        )

else:
    st.info("No hay ventas registradas")