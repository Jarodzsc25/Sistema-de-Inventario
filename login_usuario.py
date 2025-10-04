usuarios = {
    "admin": "1234",
    "jarod": "abcd",
    "usuario": "clave"
}

#primero se pedira que se ingrese el usurio, seguido de la contraseña
#ahora se agrego un meno intereactivo para que el programa este funcionando sin que este finalice hasta que se decida
def login():
        while True:
            print("\n=== Sistema de Login ===")
            print("1. Iniciar sesión")
            print("2. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                usuario = input("Ingrese su usuario: ")
                contraseña = input("Ingrese su contraseña: ")

                if usuario in usuarios and usuarios[usuario] == contraseña:
                    print(f"Bienvenido {usuario}, acceso concedido.")
                else:
                    print("Usuario o contraseña incorrectos.")

            elif opcion == "2":
                print("Cerrando el sistema.")
                break
            else:
                print("Opción inválida, intente de nuevo.")
if __name__ == "__main__":
    login()