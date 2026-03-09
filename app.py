import json
import os
import streamlit as st

def load_users():
    if os.path.exists("users.json"):
        with open("users.json","r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f)
        
st.set_page_config(page_title="Mis Macros")

st.title("Mis Macros")

menu = st.sidebar.selectbox(
    "Menú",
    ["Login", "Registro", "Dashboard"]
)

users = load_users()

if menu == "Login":
    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):
        if email in users and users[email] == password:
            st.session_state["user"] = email
            st.success("Login correcto")
        else:
            st.error("Usuario o contraseña incorrectos")

elif menu == "Registro":
    st.header("Crear cuenta")

    email = st.text_input("Nuevo email")
    password = st.text_input("Nueva contraseña", type="password")

    if st.button("Registrar"):
        if email in users:
            st.error("El usuario ya existe")
        else:
            users[email] = password
            save_users(users)
            st.success("Cuenta creada")

elif menu == "Dashboard":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")
    else:
        st.header("Dashboard")
        st.write("Usuario:", st.session_state["user"])
        st.write("Aquí aparecerán tus macros")
