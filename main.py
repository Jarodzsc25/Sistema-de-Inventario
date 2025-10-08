from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

# ============================================================
# 🔌 Conexión a la base de datos PostgreSQL
# ============================================================
def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="prueba",
        user="postgres",
        password="latorrededruaka",  # 🔒 reemplaza por la tuya
        port="5432"
    )

# ============================================================
# 🚀 Configuración de FastAPI
# ============================================================
app = FastAPI(title="API Sistema de Ventas", description="API conectada a PostgreSQL", version="1.0")

# ============================================================
# 🧱 Modelo de datos (para las peticiones JSON)
# ============================================================
class Cliente(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: str | None = None
    direccion: str | None = None


# ============================================================
# 🧩 RUTAS DE LA API
# ============================================================

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API del sistema de ventas"}

# -------------------------------
# MOSTRAR TODOS LOS CLIENTES
# -------------------------------
@app.get("/clientes")
def obtener_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cliente;")
    clientes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return {"clientes": clientes}


# -------------------------------
# AGREGAR CLIENTE
# -------------------------------
@app.post("/clientes")
def agregar_cliente(cliente: Cliente):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO cliente (nombre, apellido, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s);
        """, (cliente.nombre, cliente.apellido, cliente.correo, cliente.telefono, cliente.direccion))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "✅ Cliente agregado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# ELIMINAR CLIENTE POR ID
# -------------------------------
@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM cliente WHERE id_cliente = %s;", (id_cliente,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": f"🗑️ Cliente con id {id_cliente} eliminado correctamente"}
