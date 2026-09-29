# src/utils/configuracion.py

class Configuracion:
    # Variable privada que almacena la única instancia
    _instancia = None

    # Controla la creación de la instancia de la clase
    def __new__(cls):
        # Crea la instancia si no existe
        if cls._instancia is None:
            cls._instancia = super(Configuracion, cls).__new__(cls)
            # Inicialización del diccionario de configuraciones
            cls._instancia._configuraciones = {
                "nombre_hospital": "Policlínico Juan José Rodríguez Lazo",
                "ruta_bd": "data/hospital.db",
                "tema_gui": "light"
            }
        # Retorna la instancia existente
        return cls._instancia

    # Método estático para obtener la instancia única
    @staticmethod
    def get_instance():
        if Configuracion._instancia is None:
            Configuracion()
        return Configuracion._instancia

    # Obtiene un valor de configuración por su clave
    def obtener(self, clave):
        # Retorna el valor o 'No encontrado' por defecto
        return self._configuraciones.get(clave, "No encontrado")

    # Actualiza o crea un valor de configuración
    def actualizar(self, clave, valor):
        self._configuraciones[clave] = valor
        return True