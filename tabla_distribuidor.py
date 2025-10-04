def agregar_distribuidor(conexion, cursor):
    nombre_empresa = input("Nombre de la empresa: ")
    contacto = input("Contacto (opcional): ") or None
    telefono = input("Teléfono (opcional): ") or None
    direccion = input("Dirección (opcional): ") or None
    try:
        cursor.execute("""
            INSERT INTO distribuidor (nombre_empresa, contacto, telefono, direccion)
            VALUES (%s, %s, %s, %s)
        """, (nombre_empresa, contacto, telefono, direccion))
        conexion.commit()
        print("Distribuidor agregado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def buscar_distribuidor(conexion, cursor):
    nombre_empresa = input("Nombre de la empresa: ")
    cursor.execute("SELECT * FROM distribuidor WHERE nombre_empresa=%s", (nombre_empresa,))
    distribuidor = cursor.fetchone()
    print(distribuidor if distribuidor else "⚠ Distribuidor no encontrado.")


def actualizar_distribuidor(conexion, cursor):
    id_distribuidor = input("ID del distribuidor a actualizar: ")
    nombre_empresa = input("Nuevo nombre (opcional): ") or None
    contacto = input("Nuevo contacto (opcional): ") or None
    telefono = input("Nuevo teléfono (opcional): ") or None
    direccion = input("Nueva dirección (opcional): ") or None

    campos = []
    valores = []
    if nombre_empresa: campos.append("nombre_empresa=%s"); valores.append(nombre_empresa)
    if contacto: campos.append("contacto=%s"); valores.append(contacto)
    if telefono: campos.append("telefono=%s"); valores.append(telefono)
    if direccion: campos.append("direccion=%s"); valores.append(direccion)
    valores.append(id_distribuidor)

    if campos:
        sql = f"UPDATE distribuidor SET {', '.join(campos)} WHERE id_distribuidor=%s"
        try:
            cursor.execute(sql, tuple(valores))
            conexion.commit()
            print("Distribuidor actualizado.")
        except Exception as e:
            conexion.rollback()
            print("Error:", e)
    else:
        print("⚠ No se actualizaron campos.")


def eliminar_distribuidor(conexion, cursor):
    id_distribuidor = input("ID del distribuidor a eliminar: ")
    try:
        cursor.execute("DELETE FROM distribuidor WHERE id_distribuidor=%s", (id_distribuidor,))
        conexion.commit()
        print("Distribuidor eliminado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def listar_distribuidores(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM distribuidor ORDER BY id_distribuidor")
        distribuidores = cursor.fetchall()
        if not distribuidores:
            print("No hay distribuidores registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE DISTRIBUIDORES ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in distribuidores:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar distribuidores:", e)


def menu_distribuidores(conexion, cursor):
    while True:
        print("\n=== MENÚ DISTRIBUIDORES ===")
        print("1. Agregar distribuidor")
        print("2. Buscar distribuidor")
        print("3. Actualizar distribuidor")
        print("4. Eliminar distribuidor")
        print("5. Listar todos los distribuidores")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_distribuidor(conexion, cursor)
        elif opcion == "2":
            buscar_distribuidor(conexion, cursor)
        elif opcion == "3":
            actualizar_distribuidor(conexion, cursor)
        elif opcion == "4":
            eliminar_distribuidor(conexion, cursor)
        elif opcion == "5":
            listar_distribuidores(conexion, cursor)
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
