def agregar_recibo(conexion, cursor):
    id_pedido = int(input("ID del pedido: "))
    metodo_pago = input("Método de pago: ")
    try:
        cursor.execute("""
            INSERT INTO recibo (id_pedido, metodo_pago)
            VALUES (%s, %s)
        """, (id_pedido, metodo_pago))
        conexion.commit()
        print("Recibo agregado.")
    except Exception as e:
        conexion.rollback()
        print("Error al agregar recibo:", e)


def listar_recibos(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM recibo ORDER BY id_recibo")
        recibos = cursor.fetchall()
        if not recibos:
            print("No hay recibos registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE RECIBOS ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in recibos:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar recibos:", e)


def menu_recibos(conexion, cursor):
    while True:
        print("\n=== MENÚ RECIBOS ===")
        print("1. Agregar recibo")
        print("2. Listar todos los recibos")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_recibo(conexion, cursor)
        elif opcion == "2":
            listar_recibos(conexion, cursor)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")
