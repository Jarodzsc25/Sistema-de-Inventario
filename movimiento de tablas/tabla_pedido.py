def agregar_pedido(conexion, cursor):
    id_cliente = int(input("ID del cliente: "))
    id_empleado = int(input("ID del empleado: "))
    estado = input("Estado del pedido (Pendiente por defecto): ") or "Pendiente"
    try:
        cursor.execute("""
            INSERT INTO pedido (id_cliente, id_empleado, estado)
            VALUES (%s, %s, %s) RETURNING id_pedido
        """, (id_cliente, id_empleado, estado))
        id_pedido = cursor.fetchone()[0]
        conexion.commit()
        print(f"Pedido agregado con ID: {id_pedido}")
    except Exception as e:
        conexion.rollback()
        print("Error al agregar pedido:", e)


def eliminar_pedido(conexion, cursor):
    id_pedido = int(input("ID del pedido a eliminar: "))
    try:
        cursor.execute("DELETE FROM pedido WHERE id_pedido=%s", (id_pedido,))
        conexion.commit()
        print("Pedido eliminado.")
    except Exception as e:
        conexion.rollback()
        print("Error al eliminar pedido:", e)


def listar_pedidos(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM pedido ORDER BY id_pedido")
        pedidos = cursor.fetchall()
        if not pedidos:
            print("No hay pedidos registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE PEDIDOS ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in pedidos:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar pedidos:", e)


def menu_pedidos(conexion, cursor):
    while True:
        print("\n=== MENÚ PEDIDOS ===")
        print("1. Agregar pedido")
        print("2. Eliminar pedido")
        print("3. Listar todos los pedidos")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_pedido(conexion, cursor)
        elif opcion == "2":
            eliminar_pedido(conexion, cursor)
        elif opcion == "3":
            listar_pedidos(conexion, cursor)
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
