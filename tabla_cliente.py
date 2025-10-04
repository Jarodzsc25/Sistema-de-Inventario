# Funciones CRUD y listar clientes
def agregar_cliente(conexion, cursor):
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    correo = input("Correo: ")
    telefono = input("Teléfono (opcional): ") or None
    direccion = input("Dirección (opcional): ") or None
    try:
        cursor.execute("""
            INSERT INTO cliente (nombre, apellido, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, correo, telefono, direccion))
        conexion.commit()
        print("Cliente agregado correctamente.")
    except Exception as e:
        conexion.rollback()
        print("Error al agregar cliente:", e)


def buscar_cliente(conexion, cursor):
    correo = input("Correo del cliente: ")
    cursor.execute("SELECT * FROM cliente WHERE correo=%s", (correo,))
    cliente = cursor.fetchone()
    print(cliente if cliente else "⚠ Cliente no encontrado.")


def actualizar_cliente(conexion, cursor):
    id_cliente = input("ID del cliente a actualizar: ")
    nombre = input("Nuevo nombre (dejar en blanco si no cambia): ") or None
    apellido = input("Nuevo apellido: ") or None
    correo = input("Nuevo correo: ") or None
    telefono = input("Nuevo teléfono: ") or None
    direccion = input("Nueva dirección: ") or None

    campos = []
    valores = []
    if nombre: campos.append("nombre=%s"); valores.append(nombre)
    if apellido: campos.append("apellido=%s"); valores.append(apellido)
    if correo: campos.append("correo=%s"); valores.append(correo)
    if telefono: campos.append("telefono=%s"); valores.append(telefono)
    if direccion: campos.append("direccion=%s"); valores.append(direccion)
    valores.append(id_cliente)

    if campos:
        sql = f"UPDATE cliente SET {', '.join(campos)} WHERE id_cliente=%s"
        try:
            cursor.execute(sql, tuple(valores))
            conexion.commit()
            print("Cliente actualizado correctamente.")
        except Exception as e:
            conexion.rollback()
            print("Error al actualizar:", e)
    else:
        print("⚠ No se actualizaron campos.")


def eliminar_cliente(conexion, cursor):
    id_cliente = input("ID del cliente a eliminar: ")
    try:
        cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
        conexion.commit()
        print("Cliente eliminado correctamente.")
    except Exception as e:
        conexion.rollback()
        print("Error al eliminar cliente:", e)


def listar_clientes(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM cliente ORDER BY id_cliente")
        clientes = cursor.fetchall()

        if not clientes:
            print("No hay clientes registrados.")
            return

        # Nombres de columnas automáticos
        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE CLIENTES ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in clientes:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))

    except Exception as e:
        print("Error al listar clientes:", e)


def menu_clientes(conexion, cursor):
    while True:
        print("\n=== GESTIÓN DE CLIENTES ===")
        print("1. Agregar cliente")
        print("2. Buscar cliente")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Volver al menú principal")
        print("6. Listar todos los clientes")  # nueva opción

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_cliente(conexion, cursor)
        elif opcion == "2":
            buscar_cliente(conexion, cursor)
        elif opcion == "3":
            actualizar_cliente(conexion, cursor)
        elif opcion == "4":
            eliminar_cliente(conexion, cursor)
        elif opcion == "5":
            break
        elif opcion == "6":
            listar_clientes(conexion, cursor)
        else:
            print("Opción inválida.")
