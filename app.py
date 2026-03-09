import streamlit as st
import os
import json
from datetime import date

# -----------------------------
# RUTAS Y JSON
# -----------------------------
USERS_FILE = "users.json"
FOODS_FILE = "foods.json"
DIARY_FILE = "diary.json"

def init_json(file_path, default_data):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(default_data, f)

# Inicializar JSON si no existen
init_json(USERS_FILE, {})
init_json(FOODS_FILE, {})
init_json(DIARY_FILE, {})

# -----------------------------
# FUNCIONES DE CARGA Y GUARDADO
# -----------------------------
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_foods():
    with open(FOODS_FILE, "r") as f:
        return json.load(f)

def save_foods(foods):
    with open(FOODS_FILE, "w") as f:
        json.dump(foods, f, indent=4)

def load_diary():
    with open(DIARY_FILE, "r") as f:
        return json.load(f)

def save_diary(diary):
    with open(DIARY_FILE, "w") as f:
        json.dump(diary, f, indent=4)

# -----------------------------
# SESIÓN
# -----------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# -----------------------------
# MENÚ PRINCIPAL
# -----------------------------
menu = st.sidebar.selectbox("Menú", ["Login", "Registro", "Perfil", "Diario"])

# -----------------------------
# LOGIN
# -----------------------------
if menu == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        users = load_users()

        if email in users:
            if not isinstance(users[email], dict):
                users[email] = {}
            if users[email].get("password") == password:
                st.session_state["user"] = email
                st.success("Login correcto")
            else:
                st.error("Contraseña incorrecta")
        else:
            st.error("Usuario no registrado")

# -----------------------------
# REGISTRO
# -----------------------------
elif menu == "Registro":
    st.header("Registro de usuario")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrar"):
        users = load_users()
        if email in users:
            st.warning("El usuario ya existe")
        else:
            users[email] = {"password": password}
            save_users(users)
            st.success("Usuario registrado correctamente")

# -----------------------------
# PERFIL
# -----------------------------
elif menu == "Perfil":
    if st.session_state["user"] is None:
        st.warning("Primero inicia sesión")
    else:
        st.header("Perfil")
        user = st.session_state["user"]
        users = load_users()
        if not isinstance(users.get(user), dict):
            users[user] = {}

        peso = st.number_input("Peso (kg)", value=users[user].get("peso", 70))
        altura = st.number_input("Altura (cm)", value=users[user].get("altura", 170))
        edad = st.number_input("Edad", value=users[user].get("edad", 30))
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=0 if users[user].get("sexo","Hombre")=="Hombre" else 1)
        actividad = st.selectbox("Nivel de actividad", ["Sedentaria", "Ligera", "Moderada", "Alta", "Muy alta"], index=0)

        if st.button("Guardar perfil"):
            users[user]["peso"] = peso
            users[user]["altura"] = altura
            users[user]["edad"] = edad
            users[user]["sexo"] = sexo
            users[user]["actividad"] = actividad
            save_users(users)
            st.success("Perfil guardado")

# -----------------------------
# DIARIO
# -----------------------------
elif menu == "Diario":
    if st.session_state["user"] is None:
        st.warning("Primero inicia sesión")
    else:
        st.header("Registro diario")
        user = st.session_state["user"]
        foods = load_foods()
        diary = load_diary()

        # Inicializar estructuras si no existen
        if user not in diary:
            diary[user] = {}

        # Selector de fecha
        fecha = st.date_input("Fecha", value=date.today()).isoformat()
        if fecha not in diary[user]:
            diary[user][fecha] = []

        # Añadir alimento
        if len(foods) == 0:
            st.warning("Primero añade alimentos")
        else:
            alimento = st.selectbox("Seleccionar alimento", list(foods.keys()))
            cantidad = st.number_input("Cantidad (porciones)", 0.0, 10.0, 1.0)
            if st.button("Añadir comida"):
                diary[user][fecha].append({"food": alimento, "cantidad": cantidad})
                save_diary(diary)
                st.success(f"{alimento} añadido al {fecha}")

        # Mostrar alimentos del día
        st.subheader(f"Alimentos registrados - {fecha}")
        if len(diary[user][fecha]) == 0:
            st.info("No hay alimentos registrados para este día")
        else:
            for i, item in enumerate(diary[user][fecha]):
                col1, col2, col3 = st.columns([4,2,2])
                with col1:
                    st.write(f"{item['food']}")
                with col2:
                    st.write(f"{item['cantidad']}")
                with col3:
                    if st.button(f"Eliminar {i}"):
                        diary[user][fecha].pop(i)
                        save_diary(diary)
                        st.experimental_rerun()
