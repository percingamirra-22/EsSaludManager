import tkinter as tk
from tkinter import ttk
# Importamos tu Singleton de configuración
from src.utils.configuracion import Configuracion 

class VentanaPrincipal:
    def __init__(self):
        # Crear la ventana base
        self.root = tk.Tk()
        
        # Obtener el nombre del hospital desde tu configuración
        config = Configuracion.get_instance()
        nombre_hospital = config.obtener("nombre_hospital")
        
        # Configurar la ventana (título y tamaño)
        self.root.title(f"Sistema de Gestión - {nombre_hospital}")
        self.root.geometry("800x600")
        
        # Crear un título de texto en la ventana
        titulo = tk.Label(self.root, text=nombre_hospital, font=("Arial", 20, "bold"))
        titulo.pack(pady=30)
        
        # Crear un contenedor para los botones
        marco_botones = ttk.Frame(self.root)
        marco_botones.pack(pady=20)
        
        # Crear los botones de los módulos principales
        btn_citas = ttk.Button(marco_botones, text="Gestión de Citas", command=self.abrir_citas)
        btn_citas.grid(row=0, column=0, padx=10)
        
        btn_historial = ttk.Button(marco_botones, text="Historial Clínico", command=self.abrir_historial)
        btn_historial.grid(row=0, column=1, padx=10)
        
        btn_medicamentos = ttk.Button(marco_botones, text="Medicamentos", command=self.abrir_medicamentos)
        btn_medicamentos.grid(row=0, column=2, padx=10)

    # Funciones de prueba para los botones
    def abrir_citas(self):
        print("Abriendo módulo de citas...")

    def abrir_historial(self):
        print("Abriendo módulo de historial...")

    def abrir_medicamentos(self):
        print("Abriendo módulo de medicamentos...")

    # Arrancar la interfaz
    def iniciar(self):
        self.root.mainloop()

# Esto permite probar la ventana suelta
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.iniciar()