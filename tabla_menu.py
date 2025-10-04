from tabla_conexion import conectar_bd
from login_usuario import login
from tabla_cliente import menu_clientes

def interfaz_principal():
    conexion, cursor = conectar_bd()
    if not conexion:
        return

    while True:
        print("\n=== INTERFAZ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = login()
            if usuario:
                while True:
                    print(f"\n=== MENÚ PRINCIPAL ({usuario}) ===")
                    print("1. Gestionar clientes")
                    print("2. Cerrar sesión")
                    sub_opcion = input("Seleccione una opción: ")

                    if sub_opcion == "1":
                        menu_clientes(conexion, cursor)
                    elif sub_opcion == "2":
                        print(f"Sesión cerrada para {usuario}.")
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
