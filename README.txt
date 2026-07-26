# 1. Clonar o descargar
cd practico2

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Levantar servidor (en una terminal dedicada del archivo main.py)
uvicorn main:app --reload --port 8001

# 4. Ejecutar cliente (en otra terminal dedicada del archivo cliente/cliente.py)
cd cliente
python cliente.py