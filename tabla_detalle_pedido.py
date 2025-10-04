def agregar_detalle_pedido(conexion, cursor):
    id_pedido = int(input("ID del pedido: "))
    id_producto = int(input("ID del producto: "))
    cantidad = int(input("Cantidad: "))
    try:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
            VALUES (%s, %s, %s)
        """, (id_pedido, id_producto, cantidad))
        conexion.commit()
        print("Detalle del pedido agregado.")
    except Exception as e:
        conexion.rollback()
        print("Error al agregar detalle:", e)


def listar_detalles(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM detalle_pedido ORDER BY id_detalle")
        detalles = cursor.fetchall()
        if not detalles:
            print("No hay detalles de pedidos registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE DETALLES DE PEDIDOS ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in detalles:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar detalles:", e)


def menu_detalle_pedido(conexion, cursor):
    while True:
        print("\n=== MENÚ DETALLE PEDIDO ===")
        print("1. Agregar detalle")
        print("2. Listar todos los detalles")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_detalle_pedido(conexion, cursor)
        elif opcion == "2":
            listar_detalles(conexion, cursor)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")
