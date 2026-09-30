# src/gui/ventanas/ventana_medicamentos.py
import tkinter as tk
from tkinter import ttk
from src.utils.logger import LogSistema

class VentanaMedicamentos:
    def __init__(self, ventana_padre):
        self.window = tk.Toplevel(ventana_padre)
        self.window.title("Stock de Medicamentos")
        self.window.geometry("400x300")
        
        self.logger = LogSistema.get_instance()

        ttk.Label(self.window, text="Inventario", font=("Arial", 14, "bold")).pack(pady=15)

        # Una lista de prueba (Treeview es la tabla de Tkinter)
        columnas = ("codigo", "nombre", "stock")
        tabla = ttk.Treeview(self.window, columns=columnas, show="headings")
        
        tabla.heading("codigo", text="Código")
        tabla.heading("nombre", text="Medicamento")
        tabla.heading("stock", text="Stock")
        
        # Ajustamos tamaños de columnas
        tabla.column("codigo", width=80)
        tabla.column("nombre", width=150)
        tabla.column("stock", width=80)

        # Insertamos datos falsos (Mockup) para que la interfaz no se vea vacía
        tabla.insert("", tk.END, values=("MED-001", "Paracetamol 500mg", "150"))
        tabla.insert("", tk.END, values=("MED-002", "Amoxicilina", "45"))
        
        tabla.pack(pady=10)