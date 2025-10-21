import psycopg2
from contextlib import contextmanager

# ----------------------------------------------------------------------------------
# !!! IMPORTANTE: REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE POSTGRESQL !!!
# ----------------------------------------------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'bd_ventas',
    'user': 'postgres',
    'password': 'latorrededruaka',
    'port': '5432'
}
# ----------------------------------------------------------------------------------

@contextmanager
def get_db_connection():
    """
    Establece una conexión a la base de datos PostgreSQL usando context manager.
    Asegura que la conexión se cierre automáticamente.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        # En una aplicación real, se manejaría este error de forma más robusta
        raise
    finally:
        if conn:
            conn.close()

def execute_query(sql, params=None, fetch=False):
    """
    Ejecuta una consulta SQL genérica.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, params)
                if fetch:
                    # Si fetch=True, intenta obtener resultados
                    if cur.description:
                        # Obtener nombres de columnas
                        column_names = [desc[0] for desc in cur.description]
                        # Obtener resultados como lista de diccionarios
                        results = [dict(zip(column_names, row)) for row in cur.fetchall()]
                        return results
                    return []
                # Commit si la operación es de modificación (INSERT, UPDATE, DELETE)
                conn.commit()
                return cur.rowcount if not fetch else None
            except psycopg2.Error as e:
                # Rollback en caso de error
                conn.rollback()
                print(f"Error en la consulta SQL: {e}")
                # Re-lanzar la excepción para que Flask la maneje
                raise

