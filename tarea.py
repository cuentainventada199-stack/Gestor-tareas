class Tarea:
    """Representa una tarea con atributos privados y acceso controlado."""
    def __init__(self, identificador, titulo, completada=False):
        self.__id = int(identificador)
        self.set_titulo(titulo)
        self.__completada = bool(completada)

    def get_id(self):
        return self.__id

    def get_titulo(self):
        return self.__titulo

    def set_titulo(self, titulo):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError('El título no puede estar vacío.')
        if len(titulo.strip()) > 100:
            raise ValueError('El título no puede superar 100 caracteres.')
        self.__titulo = titulo.strip()

    def get_completada(self):
        return self.__completada

    def set_completada(self, completada):
        if not isinstance(completada, bool):
            raise ValueError('El estado debe ser verdadero o falso.')
        self.__completada = completada

    def a_diccionario(self):
        return {'id': self.__id, 'titulo': self.__titulo, 'completada': self.__completada}

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos['id'], datos['titulo'], datos['completada'])
