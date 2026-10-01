"""Repositorio en memoria. Se puede reemplazar por uno con BD/JSON
manteniendo los mismos métodos (guardar, obtener, listar, eliminar)."""


class RepositorioMemoria:
    def __init__(self):
        self._datos = {}
        self._siguiente = 1

    def guardar(self, entidad):
        if not entidad.id:
            entidad.id = self._siguiente
            self._siguiente += 1
        self._datos[entidad.id] = entidad
        return entidad

    def obtener(self, id_):
        return self._datos.get(id_)

    def listar(self):
        return list(self._datos.values())

    def eliminar(self, id_) -> bool:
        return self._datos.pop(id_, None) is not None
