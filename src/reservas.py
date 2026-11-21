"""
Módulo de gestión de reservas para Software FJ.
Integra Cliente y Servicio dentro de la clase Reserva, implementando
estados controlados, encadenamiento de excepciones y bloques try/except/else/finally.
"""

from src.entidades import EntidadSistema, Cliente
from src.servicios import Servicio
from src.excepciones import (
    ErrorDatosInvalidos,
    ErrorOperacionNoPermitida,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorCalculoInconsistente,
)
from src.logger import logger


class Reserva(EntidadSistema):
    """
    Representa una reserva de un servicio por parte de un cliente.
    Gestiona su ciclo de vida: PENDIENTE -> CONFIRMADA -> PROCESADA (o CANCELADA).
    """

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(id_reserva)

        # Validación de tipos y reglas de negocio antes de crear la reserva
        if not isinstance(cliente, Cliente):
            raise ErrorDatosInvalidos("Debe proporcionar una instancia válida de Cliente.")
        if not cliente.activo:
            raise ErrorOperacionNoPermitida(f"El cliente '{cliente.nombre}' está inactivo y no puede reservar.")
        if not isinstance(servicio, Servicio):
            raise ErrorDatosInvalidos("Debe proporcionar una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(f"El servicio '{servicio.nombre}' no está disponible actualmente.")

        # Encadenamiento de excepciones: si la duración falla en el servicio,
        # se envuelve como ErrorReservaInvalida conservando la causa original.
        try:
            servicio.validar_parametros(duracion)
        except ErrorDatosInvalidos as exc_original:
            logger.error(f"Fallo de validación al crear reserva {id_reserva}: {exc_original}")
            raise ErrorReservaInvalida(
                f"No se pudo crear la reserva {id_reserva} por duración inválida ({duracion})."
            ) from exc_original

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = float(duracion)
        self.__estado = "PENDIENTE"
        self.__costo_final = 0.0

        logger.info(
            f"Reserva creada [{self.id}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion}"
        )

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion(self) -> float:
        return self.__duracion

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_final(self) -> float:
        return self.__costo_final

    def confirmar(self) -> bool:
        """
        Confirma una reserva en estado PENDIENTE.
        Demuestra el uso de try / except / else.
        """
        try:
            if self.__estado != "PENDIENTE":
                raise ErrorOperacionNoPermitida(
                    f"No se puede confirmar la reserva {self.id} porque está en estado '{self.__estado}'."
                )
            if not self.__servicio.disponible:
                raise ErrorServicioNoDisponible(
                    f"El servicio '{self.__servicio.nombre}' dejó de estar disponible."
                )
        except (ErrorOperacionNoPermitida, ErrorServicioNoDisponible) as e:
            logger.error(f"Error al confirmar reserva {self.id}: {e}")
            raise
        else:
            # Solo se ejecuta si no hubo ninguna excepción en el bloque try
            self.__estado = "CONFIRMADA"
            logger.info(f"Reserva {self.id} confirmada exitosamente.")
            return True

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Procesa una reserva CONFIRMADA y calcula su costo final.
        Demuestra el uso de try / except / finally y encadenamiento de excepciones.
        """
        logger.info(f"Iniciando procesamiento de reserva {self.id}...")
        try:
            if self.__estado != "CONFIRMADA":
                raise ErrorOperacionNoPermitida(
                    f"La reserva {self.id} debe estar CONFIRMADA para procesarse (estado actual: {self.__estado})."
                )

            # Invocación polimórfica y sobrecargada de calcular_costo
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto=impuesto, descuento=descuento)
            self.__costo_final = costo
            self.__estado = "PROCESADA"
            logger.info(f"Reserva {self.id} procesada. Costo final: ${self.__costo_final:,.2f}")
            return self.__costo_final

        except ErrorCalculoInconsistente as exc_calculo:
            logger.error(f"Error de cálculo procesando reserva {self.id}: {exc_calculo}")
            raise ErrorReservaInvalida(
                f"Fallo financiero al procesar la reserva {self.id}."
            ) from exc_calculo

        except ErrorOperacionNoPermitida as e:
            logger.error(f"Operación no permitida en reserva {self.id}: {e}")
            raise

        finally:
            # Se ejecuta siempre, haya ocurrido error o no
            logger.info(f"Fin del intento de procesamiento para reserva {self.id} (Estado actual: {self.__estado}).")

    def cancelar(self, motivo: str = "Sin motivo especificado") -> bool:
        """
        Cancela una reserva siempre que no haya sido PROCESADA ni CANCELADA previamente.
        Demuestra el uso de try / except.
        """
        try:
            if self.__estado == "PROCESADA":
                raise ErrorOperacionNoPermitida(
                    f"No se puede cancelar la reserva {self.id} porque ya fue PROCESADA."
                )
            if self.__estado == "CANCELADA":
                raise ErrorOperacionNoPermitida(
                    f"La reserva {self.id} ya se encuentra CANCELADA."
                )

            self.__estado = "CANCELADA"
            logger.info(f"Reserva {self.id} cancelada. Motivo: {motivo}")
            return True
        except ErrorOperacionNoPermitida as e:
            logger.error(f"Error al cancelar reserva {self.id}: {e}")
            raise

    def validar(self) -> bool:
        """Valida la integridad general de la reserva."""
        if self.__estado not in self.ESTADOS_VALIDOS:
            raise ErrorReservaInvalida(f"Estado '{self.__estado}' no reconocido.")
        return True

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} | Costo final: ${self.__costo_final:,.2f}"
        )

    def __str__(self) -> str:
        return self.obtener_resumen()