import psycopg2

try:
    conectar_bd = psycopg2.connect(
        host="localhost",
        database="prueba",
        user="postgres",
        password="latorrededruaka",
        port="5432"
    )
    cursor = conectar_bd.cursor()
    print("Conectado a PostgreSQL")
except Exception as e:
    print("Error al conectar a PostgreSQL:", e)