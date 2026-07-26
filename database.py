import json
import os

DATA_FOLDER = "data"

PACIENTES_FILE = "pacientes.json"
MEDICOS_FILE = "medicos.json"
INTERNACIONES_FILE = "internaciones.json"


def cargar_datos(nombre_archivo):

    ruta = os.path.join(DATA_FOLDER, nombre_archivo)

    if not os.path.exists(ruta):
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(nombre_archivo, datos):

    ruta = os.path.join(DATA_FOLDER, nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)