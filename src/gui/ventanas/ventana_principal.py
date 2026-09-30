# src/gui/ventanas/ventana_principal.py
import tkinter as tk
from tkinter import ttk

# Importamos utilidades
from src.utils.configuracion import Configuracion 
from src.utils.logger import LogSistema 

# Importamos las ventanas secundarias que acabas de crear
from src.gui.ventanas.ventana_citas import VentanaCitas
from src.gui.ventanas.ventana_historial import VentanaHistorial
from src.gui.ventanas.ventana_medicamentos import VentanaMedicamentos

class VentanaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        
        config = Configuracion.get_instance()
        nombre_hospital = config.obtener("nombre_hospital")
        self.logger = LogSistema.get_instance()
        
        self.logger.registrar("Se inició la interfaz gráfica del sistema.", "INFO")
        
        self.root.title(f"Sistema de Gestión - {nombre_hospital}")
        self.root.geometry("800x600")
        
        titulo = tk.Label(self.root, text=nombre_hospital, font=("Arial", 20, "bold"))
        titulo.pack(pady=30)
        
        marco_botones = ttk.Frame(self.root)
        marco_botones.pack(pady=20)
        
        btn_citas = ttk.Button(marco_botones, text="Gestión de Citas", command=self.abrir_citas)
        btn_citas.grid(row=0, column=0, padx=10)
        
        btn_historial = ttk.Button(marco_botones, text="Historial Clínico", command=self.abrir_historial)
        btn_historial.grid(row=0, column=1, padx=10)
        
        btn_medicamentos = ttk.Button(marco_botones, text="Medicamentos", command=self.abrir_medicamentos)
        btn_medicamentos.grid(row=0, column=2, padx=10)

    # Funciones que abren las ventanas conectadas
    def abrir_citas(self):
        self.logger.registrar("Abriendo módulo Citas...", "INFO")
        # Le pasamos 'self.root' para que sepa quién es la ventana principal
        VentanaCitas(self.root) 

    def abrir_historial(self):
        self.logger.registrar("Abriendo módulo Historial...", "INFO")
        VentanaHistorial(self.root)

    def abrir_medicamentos(self):
        self.logger.registrar("Abriendo módulo Medicamentos...", "INFO")
        VentanaMedicamentos(self.root)

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.iniciar()