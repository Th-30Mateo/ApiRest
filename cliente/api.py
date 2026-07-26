import requests

BASE_URL = "http://127.0.0.1:8001"

TOKEN = None


def login():

    global TOKEN

    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    respuesta = requests.post(
        f"{BASE_URL}/login",
        json={
            "usuario": usuario,
            "password": password
        }
    )

    if respuesta.status_code == 200:

        TOKEN = respuesta.json()["access_token"]

        print("\nInicio de sesión exitoso.\n")

    else:

        print("\nUsuario o contraseña incorrectos.\n")


def obtener_headers():

    if TOKEN is None:
        return {}

    return {
        "Authorization": f"Bearer {TOKEN}"
    }