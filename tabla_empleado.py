def agregar_empleado(conexion, cursor):
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    cargo = input("Cargo (opcional): ") or None
    correo = input("Correo (opcional): ") or None
    telefono = input("Teléfono (opcional): ") or None
    try:
        cursor.execute("""
            INSERT INTO empleado (nombre, apellido, cargo, correo, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, cargo, correo, telefono))
        conexion.commit()
        print("Empleado agregado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def buscar_empleado(conexion, cursor):
    correo = input("Correo del empleado: ")
    cursor.execute("SELECT * FROM empleado WHERE correo=%s", (correo,))
    empleado = cursor.fetchone()
    print(empleado if empleado else "⚠ Empleado no encontrado.")


def actualizar_empleado(conexion, cursor):
    id_empleado = input("ID del empleado a actualizar: ")
    nombre = input("Nuevo nombre (opcional): ") or None
    apellido = input("Nuevo apellido (opcional): ") or None
    cargo = input("Nuevo cargo (opcional): ") or None
    correo = input("Nuevo correo (opcional): ") or None
    telefono = input("Nuevo teléfono (opcional): ") or None

    campos = []
    valores = []
    if nombre: campos.append("nombre=%s"); valores.append(nombre)
    if apellido: campos.append("apellido=%s"); valores.append(apellido)
    if cargo: campos.append("cargo=%s"); valores.append(cargo)
    if correo: campos.append("correo=%s"); valores.append(correo)
    if telefono: campos.append("telefono=%s"); valores.append(telefono)
    valores.append(id_empleado)

    if campos:
        sql = f"UPDATE empleado SET {', '.join(campos)} WHERE id_empleado=%s"
        try:
            cursor.execute(sql, tuple(valores))
            conexion.commit()
            print("Empleado actualizado.")
        except Exception as e:
            conexion.rollback()
            print("Error:", e)
    else:
        print("⚠ No se actualizaron campos.")


def eliminar_empleado(conexion, cursor):
    id_empleado = input("ID del empleado a eliminar: ")
    try:
        cursor.execute("DELETE FROM empleado WHERE id_empleado=%s", (id_empleado,))
        conexion.commit()
        print("Empleado eliminado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def listar_empleados(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM empleado ORDER BY id_empleado")
        empleados = cursor.fetchall()
        if not empleados:
            print("No hay empleados registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE EMPLEADOS ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in empleados:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar empleados:", e)


def menu_empleados(conexion, cursor):
    while True:
        print("\n=== MENÚ EMPLEADOS ===")
        print("1. Agregar empleado")
        print("2. Buscar empleado")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Listar todos los empleados")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_empleado(conexion, cursor)
        elif opcion == "2":
            buscar_empleado(conexion, cursor)
        elif opcion == "3":
            actualizar_empleado(conexion, cursor)
        elif opcion == "4":
            eliminar_empleado(conexion, cursor)
        elif opcion == "5":
            listar_empleados(conexion, cursor)
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
