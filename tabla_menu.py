# main.py
from tabla_conexion import conexion
from login_usuario import login

def interfaz_principal():
    while True:
        print("\n=== INTERFAZ PRINCIPAL ===")
        print("1. Iniciar sesión y conectar a la base de datos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = login()
            if usuario:
                conexion = conexion()
                if conexion:
                    print(f"Conexión activa. Bienvenido {usuario}.")
                    conexion.close()
                    print("Conexión cerrada correctamente.")
            else:
                print("Volviendo al menú principal...")
        elif opcion == "2":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    interfaz_principal()
