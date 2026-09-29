import datetime

class LogSistema:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(LogSistema, cls).__new__(cls)
            cls._instancia._mensajes_log = []
        return cls._instancia

    @staticmethod
    def get_instance():
        if LogSistema._instancia is None:
            LogSistema()
        return LogSistema._instancia

    def registrar(self, mensaje, nivel="INFO"):
        niveles_permitidos = ["INFO", "WARNING", "ERROR"]
        if nivel not in niveles_permitidos:
            nivel = "INFO" 

        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"[{fecha_hora}] [{nivel}] {mensaje}"
        
        self._mensajes_log.append(registro)
        print(registro)
        return True