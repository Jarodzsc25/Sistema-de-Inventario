from psycopg2 import connect, extras

DB_CONFIG = {
    "host": "localhost",
    "database": "ventas",
    "user": "postgres",
    "password": "latorrededruaka",
    "port": "5432"
}

def get_connection():
    return connect(**DB_CONFIG)
