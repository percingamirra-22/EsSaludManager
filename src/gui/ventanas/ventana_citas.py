# src/gui/ventanas/ventana_citas.py
import tkinter as tk
from tkinter import ttk

from src.utils.logger import LogSistema


class VentanaCitas:
    def __init__(self, ventana_padre):
        # Toplevel crea una ventana secundaria que se abre por encima de la principal
        self.window = tk.Toplevel(ventana_padre)
        self.window.title("Gestión de Citas")
        self.window.geometry("400x300")
        
        self.logger = LogSistema.get_instance()

        # Título
        ttk.Label(self.window, text="Registrar Nueva Cita", font=("Arial", 14, "bold")).pack(pady=15)

        # Campo para el ID del Paciente
        ttk.Label(self.window, text="DNI del Paciente:").pack(pady=5)
        self.entrada_paciente = ttk.Entry(self.window)
        self.entrada_paciente.pack(pady=5)

        # Botón de guardar
        ttk.Button(self.window, text="Guardar Cita", command=self.guardar_cita).pack(pady=20)

    def guardar_cita(self):
        paciente = self.entrada_paciente.get()
        # Registramos la acción en el logger
        self.logger.registrar(f"Se intentó guardar cita para el DNI: {paciente}", "INFO")
        print(f"Cita guardada en la interfaz para el paciente {paciente}")
        self.window.destroy() # Cierra esta ventanita al guardar