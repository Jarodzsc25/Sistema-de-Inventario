import psycopg2

try:
    conexion = psycopg2.connect(
        host="localhost",
        database="prueba",
        user="postgres",
        password="latorrededruaka",
        port="5432"
    )
    cursor = conexion.cursor()
    print("Conectado a PostgreSQL")
except Exception as e:
    print("Error al conectar a PostgreSQL:", e)