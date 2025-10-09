import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="ventas",
            user="postgres",
            password="latorrededruaka",
            port="5432"
        )
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None
