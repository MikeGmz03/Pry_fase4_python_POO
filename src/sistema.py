"""
Módulo principal de gestión en memoria para Software FJ.
Administra listas internas de clientes, servicios y reservas sin base de datos,
capturando y registrando errores para mantener el sistema operativo en todo momento.
"""

from typing import List, Optional
from src.entidades import Cliente
from src.servicios import Servicio
from src.reservas import Reserva
from src.excepciones import (
    ErrorSoftwareFJ,
    ErrorOperacionNoPermitida,
    ErrorServicioNoDisponible,
)
from src.logger import logger


class SistemaGestionFJ:
    """Orquestador en memoria de clientes, servicios y reservas de Software FJ."""

    def __init__(self):
        # Almacenamiento exclusivo en memoria mediante listas internas
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        logger.info("=== SistemaGestionFJ inicializado en memoria ===")

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente verificando que no exista un ID duplicado."""
        try:
            if any(c.id == cliente.id for c in self.__clientes):
                raise ErrorOperacionNoPermitida(f"Ya existe un cliente registrado con el ID '{cliente.id}'.")
            self.__clientes.append(cliente)
            logger.info(f"Cliente '{cliente.id}' agregado al sistema.")
            return True
        except ErrorSoftwareFJ as e:
            logger.error(f"No se pudo registrar cliente: {e}")
            raise

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra un servicio verificando que no exista un ID duplicado."""
        try:
            if any(s.id == servicio.id for s in self.__servicios):
                raise ErrorOperacionNoPermitida(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")
            self.__servicios.append(servicio)
            logger.info(f"Servicio '{servicio.id}' agregado al sistema.")
            return True
        except ErrorSoftwareFJ as e:
            logger.error(f"No se pudo registrar servicio: {e}")
            raise

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        """Busca un cliente por su ID en la lista interna."""
        return next((c for c in self.__clientes if c.id == id_cliente), None)

    def buscar_servicio(self, id_servicio: str) -> Optional[Servicio]:
        """Busca un servicio por su ID en la lista interna."""
        return next((s for s in self.__servicios if s.id == id_servicio), None)

    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: float) -> Reserva:
        """Crea y almacena una reserva validando la existencia previa de cliente y servicio."""
        cliente = self.buscar_cliente(id_cliente)
        if not cliente:
            msg = f"No se encontró el cliente con ID '{id_cliente}'."
            logger.error(msg)
            raise ErrorOperacionNoPermitida(msg)

        servicio = self.buscar_servicio(id_servicio)
        if not servicio:
            msg = f"No se encontró el servicio con ID '{id_servicio}'."
            logger.error(msg)
            raise ErrorServicioNoDisponible(msg)

        reserva = Reserva(id_reserva, cliente, servicio, duracion)
        self.__reservas.append(reserva)
        return reserva

    def generar_reporte(self) -> str:
        """Retorna un resumen general del estado actual en memoria."""
        lineas = [
            "\n" + "=" * 60,
            "REPORTE FINAL EN MEMORIA - SOFTWARE FJ",
            "=" * 60,
            f"Clientes registrados ({len(self.__clientes)}):",
            *[f"  - {c.obtener_resumen()}" for c in self.__clientes],
            f"\nServicios registrados ({len(self.__servicios)}):",
            *[f"  - {s.describir_servicio()}" for s in self.__servicios],
            f"\nReservas registradas ({len(self.__reservas)}):",
            *[f"  - {r.obtener_resumen()}" for r in self.__reservas],
            "=" * 60,
        ]
        return "\n".join(lineas)