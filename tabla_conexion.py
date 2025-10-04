import psycopg2

def conectar_bd():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="prueba",
            user="postgres",
            password="latorrededruaka",
            port="5432"
        )
        cursor = conexion.cursor()
        print("Conectado a PostgreSQL correctamente.")
        return conexion, cursor
    except Exception as e:
        print("Error al conectar a PostgreSQL:", e)
        return None, None
