"""
Aplicación principal (GUI con Tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox


class App:
    """Clase principal de la aplicación GUI"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EsSaludManager - Sistema de Gestión de Salud")
        self.root.geometry("1024x768")
        self.root.configure(bg="#f0f0f0")

        # Configurar estilo
        self._configurar_estilos()

        # Crear ventana de login
        self._crear_ventana_login()

    def _configurar_estilos(self):
        """Configurar estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use("clam")

        # Colores corporativos
        style.configure(
            "Titulo.TLabel",
            font=("Arial", 18, "bold"),
            background="#2c3e50",
            foreground="white",
        )

        style.configure("Boton.TButton", font=("Arial", 11), padding=10)

    def _crear_ventana_login(self):
        """Crear ventana de login (placeholder)"""
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        # Título
        lbl_titulo = ttk.Label(frame, text="EsSaludManager", style="Titulo.TLabel")
        lbl_titulo.pack(pady=20)

        # Mensaje de bienvenida
        lbl_mensaje = ttk.Label(
            frame,
            text="Sistema de Gestión de Salud\nVersión 1.0",
            font=("Arial", 12),
            justify="center",
        )
        lbl_mensaje.pack(pady=20)

        # Botón de inicio (placeholder)
        btn_iniciar = ttk.Button(
            frame,
            text="Iniciar Sesión",
            style="Boton.TButton",
            command=self._mostrar_login,
        )
        btn_iniciar.pack(pady=20)

        # Label de estado
        lbl_estado = ttk.Label(
            frame, text="Presiona 'Iniciar Sesión' para continuar", foreground="gray"
        )
        lbl_estado.pack(pady=10)

    def _mostrar_login(self):
        """Mostrar ventana de login (placeholder)"""
        messagebox.showinfo(
            "Login",
            "Ventana de login en desarrollo...\n\n"
            "Próximamente: autenticación de usuarios",
        )

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()
