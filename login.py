import streamlit as st
from services.auth_service import AuthService

auth_service = AuthService()

if st.session_state.get("usuario"):  # Redirige al dashboard si hay sesión activa
    st.switch_page("app.py")

# ---------------- UI -------------------------------

st.set_page_config(
    page_title="Iniciar sesión — Industrial del Sur",
    page_icon="👕",
    layout="centered"
)

st.title("👕 Industrial del Sur")
st.subheader("Iniciar sesión")
st.divider()

with st.form("form_login"):
    email = st.text_input("Email", placeholder="usuario@empresa.com")
    password = st.text_input("Contraseña", type="password")
    submit = st.form_submit_button("Ingresar", use_container_width=True)

if submit:
    ok, mensaje, usuario = auth_service.login(email, password)

    if ok:
        st.session_state["usuario"] = {
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "rol": usuario.rol.value,
            "id_sucursal": usuario.id_sucursal,
        }

        st.switch_page("app.py")
        
    else:
        st.error(mensaje)
