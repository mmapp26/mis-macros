import streamlit as st
import json
import os

st.set_page_config(page_title="Mis Macros", layout="centered")

# -----------------------
# FUNCIONES DE ARCHIVOS
# -----------------------

def load_users():
    if os.path.exists("users.json"):
        with open("users.json","r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open("users.json","w") as f:
        json.dump(data,f)

def load_foods():
    if os.path.exists("foods.json"):
        with open("foods.json","r") as f:
            return json.load(f)
    return {}

def save_foods(data):
    with open("foods.json","w") as f:
        json.dump(data,f)

def load_diary():
    if os.path.exists("diary.json"):
        with open("diary.json","r") as f:
            return json.load(f)
    return {}

def save_diary(data):
    with open("diary.json","w") as f:
        json.dump(data,f)

# -----------------------
# MENU
# -----------------------

menu = st.sidebar.selectbox(
    "Menú",
    ["Login","Registro","Perfil","Dashboard","Alimentos","Diario"]
)

# -----------------------
# REGISTRO
# -----------------------

if menu == "Registro":

    st.header("Registro")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Crear cuenta"):

        users = load_users()

        if email in users:
            st.error("El usuario ya existe")
        else:
            users[email] = {"password":password}
            save_users(users)
            st.success("Cuenta creada")

# -----------------------
# LOGIN
# -----------------------

elif menu == "Login":

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):

        users = load_users()

        if email in users and users[email]["password"] == password:
            st.session_state["user"] = email
            st.success("Login correcto")
        else:
            st.error("Credenciales incorrectas")

# -----------------------
# PERFIL
# -----------------------

elif menu == "Perfil":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")

    else:

        st.header("Perfil")

        peso = st.number_input("Peso (kg)",0.0)
        altura = st.number_input("Altura (cm)",0.0)
        edad = st.number_input("Edad",0)

        sexo = st.selectbox(
            "Sexo",
            ["Hombre","Mujer"]
        )

        actividad = st.selectbox(
            "Nivel actividad",
            ["Sedentario","Ligero","Moderado","Activo","Muy activo"]
        )

        if st.button("Guardar perfil"):

            users = load_users()
            user = st.session_state["user"]

            if not isinstance(users.get(user), dict):
                users[user] = {}

            users[user]["peso"] = peso
            users[user]["altura"] = altura
            users[user]["edad"] = edad
            users[user]["sexo"] = sexo
            users[user]["actividad"] = actividad

            save_users(users)
            st.success("Perfil guardado")
        

# -----------------------
# DASHBOARD
# -----------------------

elif menu == "Dashboard":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")

    else:

        user = st.session_state["user"]

        users = load_users()

        if "peso" not in users[user]:
            st.warning("Completa primero tu perfil")
            st.stop()

        peso = users[user]["peso"]
        altura = users[user]["altura"]
        edad = users[user]["edad"]
        sexo = users[user]["sexo"]
        actividad = users[user]["actividad"]

        foods = load_foods()
        diary = load_diary()

        total_kcal = 0
        total_p = 0
        total_g = 0
        total_c = 0
        total_f = 0

        if user in diary:

            for item in diary[user]:

                f = foods[item["food"]]
                q = item["cantidad"]

                total_kcal += f["calorias"] * q
                total_p += f["proteinas"] * q
                total_g += f["grasas"] * q
                total_c += f["carbs"] * q
                total_f += f["fibra"] * q

        # BMR

        if sexo == "Hombre":
            bmr = 10*peso + 6.25*altura - 5*edad + 5
        else:
            bmr = 10*peso + 6.25*altura - 5*edad - 161

        factores = {
            "Sedentario":1.2,
            "Ligero":1.375,
            "Moderado":1.55,
            "Activo":1.725,
            "Muy activo":1.9
        }

        tdee = bmr * factores[actividad]

        calorias_obj = tdee

        st.header("Dashboard")

        st.subheader("Calorías")

        st.write(f"{round(total_kcal)} / {round(calorias_obj)} kcal")

        st.progress(min(total_kcal/calorias_obj,1.0))

        proteina_obj = peso * 2
        grasa_obj = peso * 0.8
        carb_obj = (calorias_obj - (proteina_obj*4 + grasa_obj*9)) / 4
        fibra_obj = 30

        st.subheader("Macros")

        st.write(f"Proteínas: {round(total_p)} / {round(proteina_obj)} g")
        st.progress(min(total_p/proteina_obj,1.0))

        st.write(f"Grasas: {round(total_g)} / {round(grasa_obj)} g")
        st.progress(min(total_g/grasa_obj,1.0))

        st.write(f"Carbohidratos: {round(total_c)} / {round(carb_obj)} g")
        st.progress(min(total_c/carb_obj,1.0))

        st.write(f"Fibra: {round(total_f)} / {fibra_obj} g")
        st.progress(min(total_f/fibra_obj,1.0))

# -----------------------
# ALIMENTOS
# -----------------------

elif menu == "Alimentos":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")

    else:

        st.header("Añadir alimento")

        nombre = st.text_input("Nombre alimento")

        calorias = st.number_input("Calorías",0)
        proteinas = st.number_input("Proteínas",0.0)
        grasas = st.number_input("Grasas",0.0)
        carbs = st.number_input("Carbohidratos",0.0)
        fibra = st.number_input("Fibra",0.0)

        if st.button("Guardar alimento"):

            foods = load_foods()

            foods[nombre] = {
                "calorias":calorias,
                "proteinas":proteinas,
                "grasas":grasas,
                "carbs":carbs,
                "fibra":fibra
            }

            save_foods(foods)

            st.success("Alimento guardado")

# -----------------------
# DIARIO
# -----------------------

elif menu == "Diario":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")

    else:

        user = st.session_state["user"]
        foods = load_foods()
        diary = load_diary()

        st.header("Registro diario")

        if len(foods) == 0:
            st.warning("Primero añade alimentos")
            st.stop()

        # Selector de fecha
        from datetime import date
        fecha = st.date_input("Fecha", value=date.today()).isoformat()

        # Inicializar la fecha si no existe
        if user not in diary:
            diary[user] = {}
        if fecha not in diary[user]:
            diary[user][fecha] = []

        # Seleccionar alimento
        alimento = st.selectbox("Seleccionar alimento", list(foods.keys()))

        cantidad = st.number_input("Cantidad (porciones)", 0.0, 10.0, 1.0)

        # Botón para añadir comida
        if st.button("Añadir comida"):

            diary[user][fecha].append({
                "food": alimento,
                "cantidad": cantidad
            })

            save_diary(diary)
            st.success(f"{alimento} añadido al {fecha}")

        # Mostrar lista de alimentos del día
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
