import streamlit as st
import pandas as pd

from decimal import Decimal
from services.factura_service import FacturaService

service = FacturaService()

ID_USUARIO_SESION  = 1   # admin seedeado
ID_SUCURSAL_SESION = 1   # Casa Central seedeada

# ---------------- DATOS -------------------------------

st.title("🧾 Facturación")
st.divider()

clientes  = service.obtener_clientes_activos()   # lista de strings "id - nombre apellido"
productos = service.obtener_productos_activos()   # dict: "id - nombre" -> {id_producto, precio, stock_actual}
facturas  = service.obtener_facturas()

if "items_factura" not in st.session_state:
    st.session_state.items_factura = []

# ------------- FORMULARIO CARGAR DATOS ------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Datos de la factura")

    cliente_sel = st.selectbox("Cliente", clientes)
    tipo_factura = st.selectbox("Tipo factura", ["A", "B", "C"])
    metodo_pago = st.selectbox("Método de pago", ["EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA"])
    producto_sel = st.selectbox("Producto", list(productos.keys()))
    cantidad = st.number_input("Cantidad", min_value=1, value=1)

    prod_data = productos.get(producto_sel, {})
    stock_disponible = prod_data.get("stock_actual", 0)

    if stock_disponible <= 0:
        st.warning("⚠️ Sin stock disponible")

    if st.button("➕ Alta"):
        if stock_disponible < cantidad:
            st.error(f"Stock insuficiente. Disponible: {stock_disponible}")
        
        else:
            precio = prod_data["precio"]
            subtotal = precio * cantidad

            item = {
                "id_producto": prod_data["id_producto"],
                "producto": producto_sel,
                "precio_unitario": precio,
                "cantidad": cantidad,
                "subtotal": subtotal,
            }

            st.session_state.items_factura.append(item)
            st.rerun()

    if st.button("🧾 Generar factura"):
        if not st.session_state.items_factura:
            st.error("Debe agregar al menos un producto")

        else:
            # Extraer id_cliente del string "id - nombre apellido"
            id_cliente = int(cliente_sel.split(" - ")[0])

            ok, mensaje = service.generar_factura(
                id_cliente=id_cliente,
                id_usuario=ID_USUARIO_SESION,
                id_sucursal=ID_SUCURSAL_SESION,
                tipo_factura=tipo_factura,
                metodo_pago=metodo_pago,
                items_factura=st.session_state.items_factura,
            )

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
        df = pd.DataFrame([{
            "Producto": i["producto"],
            "Precio unitario": i["precio_unitario"],
            "Cantidad": i["cantidad"],
            "Subtotal": i["subtotal"],
        } for i in items])

        st.dataframe(df, use_container_width=True)

        total = sum(Decimal(str(i["subtotal"])) for i in items)
        iva = (total * Decimal("0.21")).quantize(Decimal("0.01"))
        
        st.metric("Subtotal", f"${total:.2f}")
        st.metric("IVA (21%)", f"${iva:.2f}")
        st.metric("TOTAL",    f"${total + iva:.2f}")

        if st.button("🗑️ Limpiar carrito"):
            st.session_state.items_factura = []
            st.rerun()

    else:
        st.info("No hay productos agregados")

# ------------- HISTORIAL ------------------

st.divider()
st.subheader("📋 Historial de facturas")

if facturas:
    # facturas devuelve: id_factura, num_factura, tipo, fecha, subtotal, impuestos, total, estado, id_venta, id_cliente
    opciones_f = {f[1]: f for f in facturas}   # clave: num_factura

    seleccionada_num = st.selectbox("Seleccionar factura", list(opciones_f.keys()))
    factura = opciones_f[seleccionada_num]

    col3, col4 = st.columns(2)

    with col3:
        st.write("**Número:**", factura[1])
        st.write("**Tipo:**", factura[2])
        st.write("**Fecha:**", factura[3])
        st.write("**Estado:**", factura[7])
    with col4:
        st.write("**Subtotal:**", f"${factura[4]}")
        st.write("**Impuestos:**", f"${factura[5]}")
        st.write("**Total:**", f"${factura[6]}")
        st.write("**ID Venta:**", factura[8])

    id_venta = factura[8]
    detalle  = service.obtener_detalle(id_venta)

    if detalle:
        df_det = pd.DataFrame(detalle, columns=["Producto", "Cantidad", "Precio", "Subtotal"])
        st.dataframe(df_det, use_container_width=True)

        contenido  = f"Factura: {factura[1]}\n"
        contenido += f"Fecha:   {factura[3]}\n"
        contenido += f"Estado:  {factura[7]}\n\n"
        contenido += "DETALLE\n"
        contenido += "-" * 50 + "\n"

        for item in detalle:
            contenido += f"{item[0]:<25} | cant: {item[1]} | ${item[2]} | ${item[3]}\n"
            contenido += "-" * 50 + "\n"
            contenido += f"Subtotal:  ${factura[4]}\n"
            contenido += f"Impuestos: ${factura[5]}\n"
            contenido += f"TOTAL:     ${factura[6]}\n"

        st.download_button(
            "📄 Descargar factura",
            data=contenido,
            file_name=f"factura_{factura[1]}.txt"
        )
        
else:
    st.info("No hay facturas registradas")