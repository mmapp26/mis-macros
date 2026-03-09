import streamlit as st

st.set_page_config(page_title="Mis Macros")

st.title("Mis Macros")

menu = st.sidebar.selectbox(
    "Menú",
    ["Login", "Registro", "Dashboard"]
)

if menu == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):
        if email == "admin@mis-macros.com" and password == "admin":
            st.success("Bienvenido Admin")
        else:
            st.error("Usuario o contraseña incorrectos")

elif menu == "Registro":
    st.header("Registro de usuario")
    st.text_input("Email")
    st.text_input("Password", type="password")
    if st.button("Crear cuenta"):
        st.success("Cuenta creada (demo)")

elif menu == "Dashboard":
    st.header("Dashboard")
    st.write("Aquí aparecerán tus macros")
