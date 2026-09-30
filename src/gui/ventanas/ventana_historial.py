# src/gui/ventanas/ventana_historial.py
import tkinter as tk
from tkinter import ttk
from src.utils.logger import LogSistema

class VentanaHistorial:
    def __init__(self, ventana_padre):
        self.window = tk.Toplevel(ventana_padre)
        self.window.title("Historial Clínico")
        self.window.geometry("400x300")
        
        self.logger = LogSistema.get_instance()

        ttk.Label(self.window, text="Buscar Historial", font=("Arial", 14, "bold")).pack(pady=15)

        ttk.Label(self.window, text="Número de Historia o DNI:").pack(pady=5)
        self.entrada_busqueda = ttk.Entry(self.window)
        self.entrada_busqueda.pack(pady=5)

        ttk.Button(self.window, text="Buscar", command=self.buscar_historial).pack(pady=20)

    def buscar_historial(self):
        busqueda = self.entrada_busqueda.get()
        self.logger.registrar(f"Buscando historial de: {busqueda}", "INFO")
        print(f"Buscando datos de {busqueda}...")
        # Aquí luego tu compañero (Persona 2) conectará la base de datos