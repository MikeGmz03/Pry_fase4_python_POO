"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Define una jerarquía clara que permite capturar errores específicos
y aplicar encadenamiento de excepciones sin detener la aplicación.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la cual heredan todos los errores del sistema."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        # Guardamos un código interno para facilitar el rastreo en los logs
        self.codigo_error = codigo_error
        self.mensaje = mensaje
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class ErrorDatosInvalidos(ErrorSoftwareFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o rango esperado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_DATOS_INVALIDOS")


class ErrorParametroFaltante(ErrorSoftwareFJ):
    """Se lanza cuando falta un argumento obligatorio para una operación."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_PARAMETRO_FALTANTE")


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Se lanza al intentar ejecutar una acción prohibida por el estado actual."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_OPERACION_NO_PERMITIDA")


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no existe o no está disponible para reservar."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_SERVICIO_NO_DISPONIBLE")


class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza ante inconsistencias al crear, confirmar o cancelar una reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_RESERVA_INVALIDA")


class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de costos, impuestos o descuentos arroja un valor inválido."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_CALCULO_INCONSISTENTE")