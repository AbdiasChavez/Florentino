class ReglaNegocioError(Exception):
    """Una operación viola una regla de negocio (RN-xx). Se responde con 409."""

    def __init__(self, mensaje: str, regla: str | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.regla = regla


class NoEncontradoError(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje
