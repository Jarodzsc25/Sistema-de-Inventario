def agregar_producto(conexion, cursor):
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))
    id_distribuidor = int(input("ID del distribuidor: "))
    try:
        cursor.execute("""
            INSERT INTO producto (nombre, descripcion, precio, stock, id_distribuidor)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, stock, id_distribuidor))
        conexion.commit()
        print("Producto agregado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def buscar_producto(conexion, cursor):
    nombre = input("Nombre del producto: ")
    cursor.execute("SELECT * FROM producto WHERE nombre=%s", (nombre,))
    producto = cursor.fetchone()
    print(producto if producto else "⚠ Producto no encontrado.")


def actualizar_producto(conexion, cursor):
    id_producto = input("ID del producto a actualizar: ")
    nombre = input("Nuevo nombre (opcional): ") or None
    descripcion = input("Nueva descripción (opcional): ") or None
    precio_input = input("Nuevo precio (opcional): ") or None
    stock_input = input("Nuevo stock (opcional): ") or None
    id_distribuidor_input = input("Nuevo ID distribuidor (opcional): ") or None

    campos = []
    valores = []
    if nombre: campos.append("nombre=%s"); valores.append(nombre)
    if descripcion: campos.append("descripcion=%s"); valores.append(descripcion)
    if precio_input: campos.append("precio=%s"); valores.append(float(precio_input))
    if stock_input: campos.append("stock=%s"); valores.append(int(stock_input))
    if id_distribuidor_input: campos.append("id_distribuidor=%s"); valores.append(int(id_distribuidor_input))
    valores.append(id_producto)

    if campos:
        sql = f"UPDATE producto SET {', '.join(campos)} WHERE id_producto=%s"
        try:
            cursor.execute(sql, tuple(valores))
            conexion.commit()
            print("Producto actualizado.")
        except Exception as e:
            conexion.rollback()
            print("Error:", e)
    else:
        print("No se actualizaron campos.")


def eliminar_producto(conexion, cursor):
    id_producto = input("ID del producto a eliminar: ")
    try:
        cursor.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
        conexion.commit()
        print("Producto eliminado.")
    except Exception as e:
        conexion.rollback()
        print("Error:", e)


def listar_productos(conexion, cursor):
    try:
        cursor.execute("SELECT * FROM producto ORDER BY id_producto")
        productos = cursor.fetchall()
        if not productos:
            print("⚠ No hay productos registrados.")
            return

        columnas = [desc[0] for desc in cursor.description]
        print("\n=== LISTA DE PRODUCTOS ===")
        print(" | ".join(col.upper().ljust(15) for col in columnas))
        print("-" * (len(columnas) * 18))

        for fila in productos:
            print(" | ".join(str(c if c is not None else "-").ljust(15) for c in fila))
    except Exception as e:
        print("Error al listar productos:", e)


def menu_productos(conexion, cursor):
    while True:
        print("\n=== MENÚ PRODUCTOS ===")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Listar todos los productos")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto(conexion, cursor)
        elif opcion == "2":
            buscar_producto(conexion, cursor)
        elif opcion == "3":
            actualizar_producto(conexion, cursor)
        elif opcion == "4":
            eliminar_producto(conexion, cursor)
        elif opcion == "5":
            listar_productos(conexion, cursor)
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
