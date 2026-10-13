# API REST — Sistema de Gestión Hospitalaria

API desarrollada con Python y FastAPI como proyecto académico para practicar diseño de endpoints HTTP, validación de datos, operaciones CRUD y autenticación mediante Bearer Token.

## Funcionalidades implementadas

- Inicio de sesión y generación de tokens de acceso.
- Gestión de pacientes: crear, listar, consultar por ID, modificar y eliminar.
- Gestión de médicos: crear, listar, consultar por ID, modificar y eliminar.
- Gestión de internaciones: registrar, listar, consultar por ID y eliminar.
- Validación de datos mediante modelos de Pydantic.
- Almacenamiento de registros en archivos JSON.
- Documentación interactiva generada por FastAPI.

> **Estado:** proyecto académico. Algunas operaciones requieren revisión y pruebas antes de considerar que todos los flujos funcionan correctamente.

## Tecnologías

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- JSON
- HTTP Bearer Authentication

## Estructura del proyecto

```text
ApiRest/
├── main.py
├── auth.py
├── database.py
├── models.py
├── routes/
│   ├── pacientes.py
│   ├── medicos.py
│   └── internaciones.py
├── cliente/
└── data/
```

Los archivos dentro de `cliente/` y los datos de `data/` pueden variar según el estado del repositorio.

## Requisitos

- Python 3.10 o superior.
- `pip`.

## Instalación

Cloná el repositorio:

```bash
git clone https://github.com/Th-30Mateo/ApiRest.git
cd ApiRest
```

Creá y activá un entorno virtual.

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalá las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde el directorio raíz del proyecto:

```bash
uvicorn main:app --reload
```

Si el servidor inicia correctamente, la API estará disponible de forma local en:

`http://127.0.0.1:8000`

La documentación interactiva se encuentra en:

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/login` | Validar credenciales y generar un token |
| POST | `/pacientes` | Crear un paciente |
| GET | `/pacientes` | Listar pacientes |
| GET | `/pacientes/{paciente_id}` | Consultar un paciente |
| PUT | `/pacientes/{paciente_id}` | Modificar un paciente |
| DELETE | `/pacientes/{paciente_id}` | Eliminar un paciente |
| POST | `/medicos` | Crear un médico |
| GET | `/medicos` | Listar médicos |
| GET | `/medicos/{medico_id}` | Consultar un médico |
| PUT | `/medicos/{medico_id}` | Modificar un médico |
| DELETE | `/medicos/{medico_id}` | Eliminar un médico |
| POST | `/internaciones` | Registrar una internación |
| GET | `/internaciones` | Listar internaciones |
| GET | `/internaciones/{internacion_id}` | Consultar una internación |
| PUT | `/internaciones/{internacion_id}` | Modificar una internación |
| DELETE | `/internaciones/{internacion_id}` | Eliminar una internación |

La presencia de una ruta en esta tabla no garantiza que su implementación funcione correctamente en todos los casos. En particular, la operación `PUT /internaciones/{internacion_id}` requiere revisión.

## Autenticación

El endpoint `POST /login` recibe un JSON con las claves `usuario` y `password`.

Ejemplo del formato esperado:

```json
{
  "usuario": "admin",
  "password": "secreto123"
}
```

Cuando las credenciales coinciden con las definidas en el código, la API devuelve un token y el tipo de autenticación:

```json
{
  "access_token": "<token_generado>",
  "token_type": "Bearer"
}
```

Para las operaciones que exigen autenticación, enviá el encabezado:

```text
Authorization: Bearer <token_generado>
```

**Advertencia:** las credenciales del ejemplo están definidas directamente en el código y son únicamente de demostración. No reutilices estas credenciales en sistemas reales.

En la implementación actual, las rutas `GET` de consulta no exigen autenticación, mientras que las operaciones de escritura utilizan la dependencia de verificación del token. Este comportamiento debería revisarse antes de cualquier uso real.

## Validación y almacenamiento

Los modelos de Pydantic definen los campos y varias restricciones de los datos recibidos. Los registros se guardan en archivos JSON dentro del directorio `data/`.

Este almacenamiento es una solución didáctica; no ofrece las garantías de integridad, concurrencia, auditoría y recuperación que se esperan de una base de datos para producción.

## Limitaciones y mejoras pendiente

- Corregir y probar las dependencias del proyecto.
- Revisar las operaciones de internaciones, especialmente la modificación.
- Unificar la política de autenticación para las rutas que lo requieran.
- Evitar credenciales codificadas en el código.
- Incorporar pruebas automatizadas de los endpoints.
- Revisar el manejo de errores de lectura y escritura de JSON.
- Evaluar el uso de una base de datos y una gestión segura de secretos si el proyecto evoluciona.

## Objetivo de aprendizaje

Practicar la creación y organización de una API REST, validación de datos, métodos HTTP, autenticación básica y persistencia mediante archivos JSON.

## Autoría y proceso de desarrollo

Proyecto académico realizado con asistencia de herramientas de IA durante el desarrollo. La utilización de este repositorio como evidencia de aprendizaje debe considerar tanto los componentes implementados como la revisión, comprensión y validación que se realicen sobre ellos.
