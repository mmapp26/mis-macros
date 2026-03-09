import json
import os
import streamlit as st

def calcular_bmr(sexo, peso, altura, edad):
    if sexo == "Hombre":
        return 10*peso + 6.25*altura - 5*edad + 5
    else:
        return 10*peso + 6.25*altura - 5*edad - 161
        
def load_users():
    if os.path.exists("users.json"):
        with open("users.json","r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f)

def load_profiles():
    if os.path.exists("profiles.json"):
        with open("profiles.json","r") as f:
            return json.load(f)
    return {}

def save_profiles(data):
    with open("profiles.json","w") as f:
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
        
st.set_page_config(page_title="Mis Macros")

st.title("Mis Macros")

menu = st.sidebar.selectbox(
    "Menú",
    ["Login","Registro","Dashboard","Alimentos","Diario"]
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

        user = st.session_state["user"]

        users = load_users()

        profile = users[user]

        peso = profile["peso"]
        altura = profile["altura"]
        edad = profile["edad"]
        sexo = profile["sexo"]
        actividad = profile["actividad"]

        # Cargar datos de alimentos y diario
        foods = load_foods()
        diary = load_diary()

        total_kcal = 0
        total_p = 0
        total_g = 0
        total_c = 0
        total_f = 0

        # Sumar alimentos del diario
        if user in diary:

            for item in diary[user]:

                f = foods[item["food"]]
                q = item["cantidad"]

                total_kcal += f["calorias"] * q
                total_p += f["proteinas"] * q
                total_g += f["grasas"] * q
                total_c += f["carbs"] * q
                total_f += f["fibra"] * q

        # Calcular metabolismo basal (Mifflin St Jeor)

        if sexo == "Hombre":
            bmr = 10*peso + 6.25*altura - 5*edad + 5
        else:
            bmr = 10*peso + 6.25*altura - 5*edad - 161

        # Factor de actividad

        factores = {
            "Sedentario":1.2,
            "Ligero":1.375,
            "Moderado":1.55,
            "Activo":1.725,
            "Muy activo":1.9
        }

        tdee = bmr * factores[actividad]

        calorias_objetivo = tdee

        st.header("Dashboard")

        # Progreso calorías

        st.subheader("Calorías")

        st.write(f"{round(total_kcal)} / {round(calorias_objetivo)} kcal")

        st.progress(min(total_kcal/calorias_objetivo,1.0))

        # Objetivos de macros

        proteina_obj = peso * 2
        grasa_obj = peso * 0.8
        carb_obj = (calorias_objetivo - (proteina_obj*4 + grasa_obj*9)) / 4
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

elif menu == "Alimentos":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")
    else:

        foods = load_foods()

        st.header("Añadir alimento")

        nombre = st.text_input("Nombre alimento")
        calorias = st.number_input("Calorías (kcal)",0)
        
        proteinas = st.number_input("Proteínas (g)",0.0)
        grasas = st.number_input("Grasas (g)",0.0)
        carbs = st.number_input("Carbohidratos (g)",0.0)
        fibra = st.number_input("Fibra (g)",0.0)

        if st.button("Guardar alimento"):

            foods[nombre] = {
                "calorias":calorias,
                "proteinas":proteinas,
                "grasas":grasas,
                "carbs":carbs,
                "fibra":fibra
            }

            save_foods(foods)

            st.success("Alimento guardado")

elif menu == "Diario":

    if "user" not in st.session_state:
        st.warning("Debes iniciar sesión")
    else:

        foods = load_foods()
        diary = load_diary()

        user = st.session_state["user"]

        st.header("Registro diario")

        alimento = st.selectbox("Seleccionar alimento", list(foods.keys()))

        cantidad = st.number_input("Cantidad (porciones)",0.0,10.0,1.0)

        if st.button("Añadir comida"):

            if user not in diary:
                diary[user] = []

            diary[user].append({
                "food":alimento,
                "cantidad":cantidad
            })

            save_diary(diary)

            st.success("Comida añadida")

        if user in diary:

            total_kcal = 0
            total_p = 0
            total_g = 0
            total_c = 0
            total_f = 0

            for item in diary[user]:

                f = foods[item["food"]]
                q = item["cantidad"]

                total_kcal += f["calorias"]*q
                total_p += f["proteinas"]*q
                total_g += f["grasas"]*q
                total_c += f["carbs"]*q
                total_f += f["fibra"]*q

            st.subheader("Totales del día")

            st.write("Calorías:",round(total_kcal),"kcal")
            
            st.write("Proteínas:",round(total_p))
            st.write("Grasas:",round(total_g))
            st.write("Carbohidratos:",round(total_c))
            st.write("Fibra:",round(total_f))
            
