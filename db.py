from psycopg2 import connect

DB_CONFIG = {
    "host": "localhost",
    "database": "ventas",
    "user": "postgres",
    "password": "latorrededruaka",
    "port": "5432"
}
##XD
def get_connection():
    return connect(**DB_CONFIG)
