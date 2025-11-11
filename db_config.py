import psycopg2
from contextlib import contextmanager

# ----------------------------------------------------------------------------------
# !!! REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE POSTGRESQL !!!
# ----------------------------------------------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'ventas',
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
        raise
    finally:
        if conn:
            conn.close()


def execute_query(sql, params=None, fetch=False):
    """
    Ejecuta una consulta SQL genérica.
    - sql: la consulta SQL con %s como placeholders
    - params: tupla de parámetros para la consulta
    - fetch: True si quieres devolver resultados (SELECT o INSERT ... RETURNING)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, params)

                # Si la operación devuelve resultados
                if fetch:
                    if cur.description:
                        # Obtener nombres de columnas
                        column_names = [desc[0] for desc in cur.description]
                        # Convertir resultados a lista de diccionarios
                        results = [dict(zip(column_names, row)) for row in cur.fetchall()]
                    else:
                        results = []
                    # Commit también en consultas con fetch (IMPORTANTE para INSERT ... RETURNING)
                    conn.commit()
                    return results

                # Commit en operaciones de modificación
                conn.commit()
                return cur.rowcount  # número de filas afectadas
            except psycopg2.Error as e:
                # Rollback en caso de error
                conn.rollback()
                print(f"Error en la consulta SQL: {e}")
                raise
