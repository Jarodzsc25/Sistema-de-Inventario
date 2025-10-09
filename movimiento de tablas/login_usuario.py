usuarios = {
    "admin": "1234",
    "jarod": "abcd",
    "usuario": "clave"
}

def login():
    print("\n=== Inicio de sesión ===")
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    if usuario in usuarios and usuarios[usuario] == contraseña:
        print(f"Bienvenido {usuario}, acceso concedido.")
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None
def validar_login_gui(usuario, contraseña):
    """Valida credenciales desde la interfaz gráfica."""
    return usuario in usuarios and usuarios[usuario] == contraseña
