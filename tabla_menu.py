from tabla_conexion import conectar_bd
from login_usuario import login
from tabla_cliente import menu_clientes
from tabla_empleado import menu_empleados
from tabla_distribuidor import menu_distribuidores
from tabla_producto import menu_productos
from tabla_pedido import menu_pedidos
from tabla_detalle_pedido import menu_detalle_pedido
from tabla_recibo import menu_recibos

def interfaz_principal():
    conexion, cursor = conectar_bd()
    if conexion is None:
        return

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = login()
            if usuario:
                while True:
                    print(f"\n=== MENÚ DEL SISTEMA ({usuario}) ===")
                    print("1. Gestionar clientes")
                    print("2. Gestionar empleados")
                    print("3. Gestionar distribuidores")
                    print("4. Gestionar productos")
                    print("5. Gestionar pedidos")
                    print("6. Gestionar detalle de pedidos")
                    print("7. Gestionar recibos")
                    print("8. Cerrar sesión")
                    sub_opcion = input("Seleccione una opción: ")

                    if sub_opcion == "1":
                        menu_clientes(conexion, cursor)
                    elif sub_opcion == "2":
                        menu_empleados(conexion, cursor)
                    elif sub_opcion == "3":
                        menu_distribuidores(conexion, cursor)
                    elif sub_opcion == "4":
                        menu_productos(conexion, cursor)
                    elif sub_opcion == "5":
                        menu_pedidos(conexion, cursor)
                    elif sub_opcion == "6":
                        menu_detalle_pedido(conexion, cursor)
                    elif sub_opcion == "7":
                        menu_recibos(conexion, cursor)
                    elif sub_opcion == "8":
                        print(f"Sesión cerrada para {usuario}")
                        break
                    else:
                        print("Opción inválida.")
        elif opcion == "2":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    interfaz_principal()
