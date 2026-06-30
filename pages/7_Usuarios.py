import streamlit as st
import pandas as pd

from services.usuario_service import UsuarioService
from services.sucursal_service import SucursalService

service = UsuarioService()
sucursal_service = SucursalService()

# ---------------- DATOS -------------------------------

st.title("👤 Gestión de Usuarios")
st.divider()

usuarios = service.obtener_todos()
sucursales = sucursal_service.obtener_todos()

suc_opciones = {s.id_sucursal: s.nombre for s in sucursales}
suc_nombres = list(suc_opciones.values())
suc_ids = list(suc_opciones.keys())

roles = ["ADMIN", "VENTAS", "COMPRAS", "CONSULTA"]

opciones = {}
if usuarios:
    opciones = {
        f"{u.id_usuario} - {u.nombre} {u.apellido} ({u.rol.value})": u
        for u in usuarios
    }

seleccionado = st.selectbox(
    "Seleccionar usuario",
    ["Nuevo usuario"] + list(opciones.keys())
)

if seleccionado != "Nuevo usuario":
    usuario = opciones[seleccionado]
    nombre_def = usuario.nombre
    apellido_def = usuario.apellido
    email_def = usuario.email
    rol_def = usuario.rol.value
    estado_def = usuario.estado
    suc_idx = suc_ids.index(usuario.id_sucursal) if usuario.id_sucursal in suc_ids else 0

else:
    usuario = None
    nombre_def = ""
    apellido_def = ""
    email_def = ""
    rol_def = "CONSULTA"
    estado_def = True
    suc_idx = 0

# ---------------- FORMULARIO -------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Formulario")

    nombre = st.text_input("Nombre",   value=nombre_def)
    apellido = st.text_input("Apellido", value=apellido_def)
    email = st.text_input("Email",    value=email_def)
    rol = st.selectbox("Rol", roles, index=roles.index(rol_def))

    suc_nombre = st.selectbox("Sucursal", suc_nombres, index=suc_idx)
    id_sucursal = suc_ids[suc_nombres.index(suc_nombre)] if suc_nombres else None

    estado = st.selectbox("Estado", ["ACTIVO", "BAJA"], index=0 if estado_def else 1)
    estado_bool = estado == "ACTIVO"

    st.markdown("---")
    st.caption("Contraseña (dejar vacío en modificación para no cambiarla)")
    password = st.text_input("Contraseña", type="password", value="")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕ Alta"):
            ok, mensaje = service.alta(nombre, apellido, email, password, rol, id_sucursal, estado_bool)
            st.success(mensaje) if ok else st.error(mensaje)
            
            if ok:
                st.rerun()

    with col_btn2:
        if st.button("✏️ Modificar"):
            if usuario is None:
                st.error("Seleccione un usuario para modificar")
            
            else:
                ok, mensaje = service.modificar(
                    usuario.id_usuario, nombre, apellido, email, rol,
                    id_sucursal, estado_bool, password=password if password else None
                )

                st.success(mensaje) if ok else st.error(mensaje)
                
                if ok:
                    st.rerun()

    with col_btn3:
        if st.button("🗑️ Baja"):
            if usuario is None:
                st.error("Seleccione un usuario para dar de baja")
            
            else:
                ok, mensaje = service.baja(usuario.id_usuario)
                st.warning(mensaje) if ok else st.error(mensaje)
                
                if ok:
                    st.rerun()

# ---------------- TABLA -------------------------------

with col2:
    st.subheader("📋 Usuarios registrados")

    if usuarios:
        df = pd.DataFrame([{
            "ID": u.id_usuario,
            "Nombre": u.nombre,
            "Apellido": u.apellido,
            "Email": u.email,
            "Rol": u.rol.value,
            "Sucursal": suc_opciones.get(u.id_sucursal, "—"),
            "Estado": "ACTIVO" if u.estado else "BAJA",
        } for u in usuarios])

        st.dataframe(df, use_container_width=True)

        st.caption("🔒 Las contraseñas nunca se muestran en la tabla.")
    
    else:
        st.info("No hay usuarios registrados")
