import tkinter as tk
from tkinter import messagebox
from tabla_conexion import conectar_bd
from login_usuario import login
from tabla_cliente import menu_clientes
from tabla_empleado import menu_empleados
from tabla_distribuidor import menu_distribuidores
from tabla_producto import menu_productos
from tabla_pedido import menu_pedidos
from tabla_detalle_pedido import menu_detalle_pedido
from tabla_recibo import menu_recibos


class AppInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.conexion, self.cursor = conectar_bd()
        if not self.conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            self.root.destroy()
            return

        self.crear_login()

    def crear_login(self):
        """Ventana de inicio de sesión"""
        self.frame_login = tk.Frame(self.root, padx=20, pady=20)
        self.frame_login.pack(expand=True)

        tk.Label(self.frame_login, text="Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.frame_login, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(self.frame_login)
        self.usuario_entry.pack()

        tk.Label(self.frame_login, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.frame_login, show="*")
        self.password_entry.pack()

        tk.Button(self.frame_login, text="Entrar", command=self.validar_login, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.frame_login, text="Salir", command=self.root.quit, bg="#f44336", fg="white").pack()

    def validar_login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        # Aquí puedes usar tu función login_usuario.py si valida desde BD o diccionario
        from login_usuario import validar_login_gui
        if validar_login_gui(usuario, password):

            messagebox.showinfo("Bienvenido", f"Acceso concedido: {usuario}")
            self.frame_login.destroy()
            self.mostrar_menu_principal(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_menu_principal(self, usuario):
        """Ventana principal del sistema"""
        self.frame_menu = tk.Frame(self.root, padx=20, pady=20)
        self.frame_menu.pack(expand=True)

        tk.Label(self.frame_menu, text=f"Bienvenido, {usuario}", font=("Arial", 14, "bold")).pack(pady=10)

        botones = [
            ("Gestionar Clientes", menu_clientes),
            ("Gestionar Empleados", menu_empleados),
            ("Gestionar Distribuidores", menu_distribuidores),
            ("Gestionar Productos", menu_productos),
            ("Gestionar Pedidos", menu_pedidos),
            ("Gestionar Detalles de Pedido", menu_detalle_pedido),
            ("Gestionar Recibos", menu_recibos),
        ]

        for texto, funcion in botones:
            tk.Button(self.frame_menu, text=texto, width=30, bg="#2196F3", fg="white",
                      command=lambda f=funcion: f(self.conexion, self.cursor)).pack(pady=3)

        tk.Button(self.frame_menu, text="Cerrar Sesión", width=30, bg="#f44336", fg="white",
                  command=self.cerrar_sesion).pack(pady=10)

    def cerrar_sesion(self):
        self.frame_menu.destroy()
        self.crear_login()


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppInventario(root)
    root.mainloop()
