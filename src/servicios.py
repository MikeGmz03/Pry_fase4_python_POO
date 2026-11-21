"""
Módulo de servicios de Software FJ.
Define la clase abstracta Servicio y tres clases derivadas especializadas
que aplican herencia, polimorfismo y sobrecarga de métodos para el cálculo de costos.
"""

from abc import abstractmethod
from src.entidades import EntidadSistema
from src.excepciones import (
    ErrorDatosInvalidos,
    ErrorParametroFaltante,
    ErrorCalculoInconsistente,
)
from src.logger import logger


class Servicio(EntidadSistema):
    """
    Clase abstracta base para todos los servicios ofrecidos por Software FJ.
    Hereda de EntidadSistema y establece el contrato polimórfico.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)

        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            raise ErrorParametroFaltante("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ErrorDatosInvalidos(f"La tarifa base ({tarifa_base}) debe ser un número mayor a 0.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    def _aplicar_ajustes_costo(self, subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Aplica impuestos y descuentos validando que el cálculo sea consistente.
        Soporta la sobrecarga lógica de calcular_costo con parámetros opcionales.
        """
        if not (0.0 <= impuesto <= 0.5):
            raise ErrorCalculoInconsistente(f"El impuesto ({impuesto}) debe estar entre 0% (0.0) y 50% (0.5).")
        if not (0.0 <= descuento <= 0.8):
            raise ErrorCalculoInconsistente(f"El descuento ({descuento}) debe estar entre 0% (0.0) y 80% (0.8).")

        monto_descuento = subtotal * descuento
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + impuesto)

        if total < 0:
            raise ErrorCalculoInconsistente("El cálculo arrojó un costo total negativo.")

        return round(total, 2)

    def validar(self) -> bool:
        """Valida los atributos generales del servicio."""
        if not self._nombre or self._tarifa_base <= 0:
            raise ErrorDatosInvalidos("El servicio tiene datos inválidos o incompletos.")
        return True

    def obtener_resumen(self) -> str:
        return self.describir_servicio()

    @abstractmethod
    def validar_parametros(self, duracion: float) -> bool:
        """Valida que la duración y reglas específicas del servicio sean correctas."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo total del servicio.
        Soporta sobrecarga mediante parámetros opcionales (solo duración, con impuesto, con descuento o ambos).
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción detallada específica de cada tipo de servicio."""
        pass


class ReservaSala(Servicio):
    """Servicio especializado para la reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, tiene_proyector: bool = False, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ErrorDatosInvalidos("La capacidad de la sala debe ser un entero positivo.")

        self._capacidad = capacidad
        self._tiene_proyector = bool(tiene_proyector)
        logger.info(f"Servicio ReservaSala creado: {self.id} - {self.nombre} (Capacidad: {self._capacidad})")

    def validar_parametros(self, duracion: float) -> bool:
        """Las salas se reservan entre 1 y 12 horas por sesión."""
        if not isinstance(duracion, (int, float)) or duracion < 1 or duracion > 12:
            raise ErrorDatosInvalidos(f"La duración para reserva de sala ({duracion}h) debe estar entre 1 y 12 horas.")
        return True

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo por hora más un recargo fijo si incluye proyector."""
        self.validar_parametros(duracion)
        recargo_proyector = 25000.0 if self._tiene_proyector else 0.0
        subtotal = (self._tarifa_base * duracion) + recargo_proyector
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        proyector = "Sí" if self._tiene_proyector else "No"
        return f"[Sala] {self.id} - {self.nombre} | Capacidad: {self._capacidad} pers. | Proyector: {proyector} | Tarifa/h: ${self._tarifa_base:,.0f}"


class AlquilerEquipo(Servicio):
    """Servicio especializado para el alquiler de hardware o equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, tipo_equipo: str, cantidad: int = 1, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not tipo_equipo or not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ErrorParametroFaltante("El tipo de equipo es obligatorio.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ErrorDatosInvalidos("La cantidad de equipos debe ser un entero mayor a 0.")

        self._tipo_equipo = tipo_equipo.strip()
        self._cantidad = cantidad
        logger.info(f"Servicio AlquilerEquipo creado: {self.id} - {self.nombre} ({self._cantidad}x {self._tipo_equipo})")

    def validar_parametros(self, duracion: float) -> bool:
        """El alquiler de equipos se mide en días (mínimo 1 día, máximo 30 días)."""
        if not isinstance(duracion, (int, float)) or duracion < 1 or duracion > 30:
            raise ErrorDatosInvalidos(f"La duración para alquiler de equipo ({duracion} días) debe estar entre 1 y 30 días.")
        return True

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo multiplicando tarifa diaria por días y cantidad de equipos."""
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion * self._cantidad
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        return f"[Equipo] {self.id} - {self.nombre} | Tipo: {self._tipo_equipo} | Cant: {self._cantidad} | Tarifa/día: ${self._tarifa_base:,.0f}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o asesoría profesional."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, nivel_senior: bool = False, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not isinstance(especialidad, str) or not especialidad.strip():
            raise ErrorParametroFaltante("La especialidad de la asesoría es obligatoria.")

        self._especialidad = especialidad.strip()
        self._nivel_senior = bool(nivel_senior)
        logger.info(f"Servicio AsesoriaEspecializada creado: {self.id} - {self.nombre} ({self._especialidad})")

    def validar_parametros(self, duracion: float) -> bool:
        """Las asesorías se agendan entre 0.5 y 8 horas."""
        if not isinstance(duracion, (int, float)) or duracion < 0.5 or duracion > 8:
            raise ErrorDatosInvalidos(f"La duración de la asesoría ({duracion}h) debe estar entre 0.5 y 8 horas.")
        return True

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo por hora aplicando un 25% adicional si el consultor es Senior."""
        self.validar_parametros(duracion)
        factor_senior = 1.25 if self._nivel_senior else 1.0
        subtotal = (self._tarifa_base * duracion) * factor_senior
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        nivel = "Senior (+25%)" if self._nivel_senior else "Estándar"
        return f"[Asesoría] {self.id} - {self.nombre} | Área: {self._especialidad} | Nivel: {nivel} | Tarifa/h: ${self._tarifa_base:,.0f}"