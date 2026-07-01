import streamlit as st
import pandas as pd

from decimal import Decimal
from services.compra_service import CompraService

service = CompraService()

# ---------------- DATOS -------------------------------

st.title("🛒 Gestión de Compras")
st.divider()

proveedores = service.obtener_proveedores_activos()
productos = service.obtener_productos_activos()
compras = service.obtener_compras()

if "items_compra" not in st.session_state:
    st.session_state.items_compra = []

# ---------------- FORMULARIO ------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Nueva compra")

    if not proveedores:
        st.warning("No hay proveedores activos. Agregue uno antes de registrar una compra.")
        st.stop()

    proveedor_sel  = st.selectbox("Proveedor", proveedores)

    num_comprobante = st.text_input(
        "N° comprobante",
        placeholder="Ej: 0001-00012345 (opcional)"
    )

    st.markdown("---")
    st.caption("Agregar productos a la orden")

    producto_sel = st.selectbox("Producto", list(productos.keys()))
    cantidad = st.number_input("Cantidad", min_value=1, value=1)

    prod_data = productos.get(producto_sel, {})

    # El precio unitario es editable: en compras el proveedor puede tener un precio distinto al precio_compra registrado en el sistema.
    precio_sugerido = float(prod_data.get("precio", 0))
    precio_unitario = st.number_input(
        "Precio unitario",
        min_value=0.0,
        value=precio_sugerido,
        format="%.2f",
        help="Se precarga con el precio de compra del producto, pero podés ajustarlo."
    )

    if st.button("➕ Agregar producto"):
        if precio_unitario <= 0:
            st.error("El precio unitario debe ser mayor a 0")
        
        else:
            precio   = Decimal(str(precio_unitario))
            subtotal = precio * cantidad

            item = {
                "id_producto": prod_data["id_producto"],
                "producto": producto_sel,
                "precio_unitario": precio,
                "cantidad": cantidad,
                "subtotal": subtotal,
            }

            st.session_state.items_compra.append(item)
            st.rerun()

    st.markdown("---")

    if st.button("✅ Registrar compra", type="primary"):
        if not st.session_state.items_compra:
            st.error("Debe agregar al menos un producto")
        
        else:
            id_proveedor = int(proveedor_sel.split(" - ")[0])

            ok, mensaje = service.registrar_compra(
                id_proveedor=id_proveedor,
                id_usuario=ID_USUARIO_SESION,
                id_sucursal=ID_SUCURSAL_SESION,
                num_comprobante=num_comprobante.strip() or None,
                items=st.session_state.items_compra,
            )

            if ok:
                st.success(mensaje)
                st.session_state.items_compra = []
                st.rerun()
            
            else:
                st.error(mensaje)

# ---------------- CARRITO ------------------------------

with col2:
    st.subheader("Detalle de la orden")

    items = st.session_state.items_compra

    if items:
        df = pd.DataFrame([{
            "Producto": i["producto"],
            "Precio unitario": f"${i['precio_unitario']:.2f}",
            "Cantidad": i["cantidad"],
            "Subtotal": f"${i['subtotal']:.2f}",
        } for i in items])

        st.dataframe(df, use_container_width=True)

        total = sum(i["subtotal"] for i in items)
        st.metric("TOTAL", f"${total:.2f}")

        if st.button("🗑️ Limpiar orden"):
            st.session_state.items_compra = []
            st.rerun()

    else:
        st.info("No hay productos agregados a la orden")

# ---------------- HISTORIAL  ------------------------------

st.divider()
st.subheader("📋 Historial de compras")

if compras:  # compras: id_compra, num_comprobante, fecha, total, razon_social
    df_hist = pd.DataFrame([{ 
        "ID": c[0],
        "N° Comprobante": c[1] or "—",
        "Fecha": c[2],
        "Total": f"${c[3]:.2f}",
        "Proveedor": c[4],
    } for c in compras])

    st.dataframe(df_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 Detalle de una compra")

    opciones_h = {
        f"#{c[0]} | {c[4]} | {c[2].strftime('%d/%m/%Y') if hasattr(c[2], 'strftime') else c[2]}": c
        for c in compras
    }

    seleccionada = st.selectbox("Seleccionar compra", list(opciones_h.keys()))
    compra = opciones_h[seleccionada]
    detalle = service.obtener_detalle_compra(compra[0])

    if detalle:
        df_det = pd.DataFrame(
            detalle,
            columns=["Producto", "Cantidad", "Precio unitario", "Subtotal"]
        )
        st.dataframe(df_det, use_container_width=True)

        fecha_str = (
            compra[2].strftime("%d/%m/%Y %H:%M")
            if hasattr(compra[2], "strftime") else str(compra[2])
        )

        contenido  = f"ORDEN DE COMPRA #{compra[0]}\n"
        contenido += f"{'=' * 40}\n"
        contenido += f"Proveedor: {compra[4]}\n"
        contenido += f"N° comprobante: {compra[1] or '—'}\n"
        contenido += f"Fecha: {fecha_str}\n\n"
        contenido += "DETALLE\n"
        contenido += f"{'-' * 50}\n"

        for item in detalle:
            contenido += f"{item[0]:<25} | cant: {item[1]:>4} | ${item[2]:>8.2f} | ${item[3]:>10.2f}\n"
            contenido += f"{'-' * 50}\n"
            contenido += f"TOTAL: ${compra[3]:.2f}\n"

        st.download_button(
            "📄 Descargar orden",
            data=contenido,
            file_name=f"compra_{compra[0]}.txt"
        )
        
else:
    st.info("No hay compras registradas")