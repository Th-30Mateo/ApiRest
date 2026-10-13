# API REST — Sistema de Gestión Hospitalaria

Proyecto académico desarrollado para practicar los conceptos de construcción de API REST con Python y FastAPI, incluyendo el manejo de datos, validación de entradas y autenticación básica.

## Objetivo

Explorar cómo organizar una API que expone operaciones relacionadas con la gestión hospitalaria y cómo interactuar con sus recursos mediante solicitudes HTTP.

## Tecnologías y conceptos

- Python
- FastAPI
- Pydantic
- HTTP y API REST
- JSON para el manejo de datos
- Autenticación basada en tokens, según la implementación actual

## Estructura

El repositorio contiene módulos relacionados con la autenticación, los clientes y los datos de la aplicación, además de otros componentes de la API.

La estructura y las responsabilidades de cada módulo pueden evolucionar a medida que se refactorice el proyecto.

## Instalación y ejecución

1. Cloná el repositorio:

```bash
git clone https://github.com/Th-30Mateo/ApiRest.git
cd ApiRest
```

2. Creá y activá un entorno virtual:

```bash
python -m venv .venv
```

En Linux o WSL:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

3. Instalá las dependencias que correspondan al proyecto. Antes de ejecutar este paso, verificá que el archivo de dependencias contenga los paquetes necesarios.

4. Si `main.py` contiene la instancia de FastAPI, ejecutá:

```bash
uvicorn main:app --reload
```

Si la aplicación utiliza otro módulo de entrada, ajustá el comando a la estructura real del proyecto.

## Estado y limitaciones

Proyecto académico en evolución. La implementación actual utiliza mecanismos de autenticación y almacenamiento adecuados para experimentar, pero que requieren mejoras antes de cualquier uso real.

En particular, las credenciales codificadas en el código, los tokens almacenados en memoria y la persistencia basada en archivos JSON no deben considerarse una solución de seguridad o almacenamiento de producción.

## Aprendizajes

- Conceptos de API REST y solicitudes HTTP.
- Organización de una aplicación Python.
- Validación de datos.
- Manejo de autenticación y tokens.
- Revisión y depuración de código con asistencia de herramientas de IA.

El uso de asistencia de IA formó parte del proceso de desarrollo. El proyecto no debe interpretarse, por sí solo, como prueba de implementación completamente autónoma de todos sus componentes.
